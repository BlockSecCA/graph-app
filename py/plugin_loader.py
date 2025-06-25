"""
Plugin Loader for Graph Analysis Plugins

Discovers and loads analysis plugins from the py/plugins/ directory.
Provides a JavaScript interface for plugin registration and execution.
"""

import sys
import importlib.util
import json
import traceback
from typing import Dict, List, Any, Optional

# Use os.path instead of pathlib for Pyodide compatibility
import os.path as path


class PluginLoader:
    """Manages discovery and loading of analysis plugins"""
    
    def __init__(self, plugins_dir: str = "py/plugins"):
        self.plugins_dir = plugins_dir
        self.loaded_plugins = {}
        self.plugin_errors = {}
    
    def discover_plugins(self) -> List[Dict[str, Any]]:
        """
        Scan plugins directory and return list of available plugins
        
        Returns:
            List of plugin info dictionaries
        """
        plugins = []
        
        import os
        if not os.path.exists(self.plugins_dir):
            print(f"Plugins directory {self.plugins_dir} does not exist")
            return plugins
        
        # Scan each subdirectory in plugins/
        import os
        for item in os.listdir(self.plugins_dir):
            plugin_dir = os.path.join(self.plugins_dir, item)
            if not os.path.isdir(plugin_dir):
                continue
                
            if item.startswith('.'):
                continue  # Skip hidden directories
                
            try:
                plugin_info = self._load_plugin_info(plugin_dir, item)
                if plugin_info:
                    plugins.append(plugin_info)
            except Exception as e:
                self.plugin_errors[item] = str(e)
                print(f"Error loading plugin {item}: {e}")
        
        return plugins
    
    def _load_plugin_info(self, plugin_dir: str, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Load plugin metadata from __init__.py"""
        import os
        init_file = os.path.join(plugin_dir, "__init__.py")
        
        if not os.path.exists(init_file):
            raise Exception(f"Plugin {plugin_name} missing __init__.py")
        
        # Add plugin directory to Python path temporarily
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)
        
        try:
            # Load the plugin module
            spec = importlib.util.spec_from_file_location(
                f"plugin_{plugin_name}", 
                init_file
            )
            
            if spec is None or spec.loader is None:
                raise Exception(f"Could not load plugin spec for {plugin_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        finally:
            # Remove from path to avoid conflicts
            if plugin_dir in sys.path:
                sys.path.remove(plugin_dir)
        
        # Extract plugin info
        if not hasattr(module, 'ANALYSIS_INFO'):
            raise Exception(f"Plugin {plugin_name} missing ANALYSIS_INFO")
        
        # Note: We don't check for analyze_graph here since it may import NetworkX
        # which isn't available in system Python, only in Pyodide
        
        plugin_info = module.ANALYSIS_INFO.copy()
        plugin_info['_module'] = module
        plugin_info['_path'] = plugin_dir
        
        # Verify analyze_graph exists in analysis.py file
        analysis_file = os.path.join(plugin_dir, "analysis.py")
        if not os.path.exists(analysis_file):
            raise Exception(f"Plugin {plugin_name} missing analysis.py file")
        
        # Validate required fields
        required_fields = ['id', 'name', 'description', 'version']
        for field in required_fields:
            if field not in plugin_info:
                raise Exception(f"Plugin {plugin_name} missing required field: {field}")
        
        self.loaded_plugins[plugin_info['id']] = plugin_info
        return plugin_info
    
    def get_plugin(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get loaded plugin by ID"""
        return self.loaded_plugins.get(plugin_id)
    
    def execute_plugin(self, plugin_id: str, nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
        """
        Execute a plugin analysis
        
        Args:
            plugin_id: ID of plugin to execute
            nodes: Graph nodes data
            edges: Graph edges data  
            parameters: Analysis parameters
            
        Returns:
            Analysis results dictionary
            
        Raises:
            Exception: If plugin not found or execution fails
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            raise Exception(f"Plugin '{plugin_id}' not found")
        
        try:
            # Import the analysis module dynamically to avoid NetworkX dependency during discovery
            plugin_dir = plugin['_path']
            import os
            analysis_file = os.path.join(plugin_dir, "analysis.py")
            
            # Load the analysis module with NetworkX available
            spec = importlib.util.spec_from_file_location(
                f"analysis_{plugin_id.replace('-', '_')}", 
                analysis_file
            )
            
            if spec is None or spec.loader is None:
                raise Exception(f"Could not load analysis module for {plugin_id}")
            
            analysis_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(analysis_module)
            
            # Call the plugin's analyze_graph function
            return analysis_module.analyze_graph(nodes, edges, parameters)
        except Exception as e:
            raise Exception(f"Plugin execution failed: {str(e)}")
    
    def get_plugin_list(self) -> List[Dict[str, Any]]:
        """Get list of loaded plugins with basic info"""
        return [
            {
                'id': info['id'],
                'name': info['name'],
                'description': info['description'],
                'version': info['version'],
                'category': info.get('category', 'other'),
                'parameters': info.get('parameters', [])
            }
            for info in self.loaded_plugins.values()
        ]


# Global plugin loader instance
_plugin_loader = None

def get_plugin_loader() -> PluginLoader:
    """Get the global plugin loader instance"""
    global _plugin_loader
    if _plugin_loader is None:
        _plugin_loader = PluginLoader()
    return _plugin_loader


# JavaScript Interface Functions
def discover_plugins_js() -> str:
    """JavaScript interface: Discover and return plugins as JSON"""
    try:
        loader = get_plugin_loader()
        plugins = loader.discover_plugins()
        return json.dumps({
            'success': True,
            'plugins': loader.get_plugin_list(),
            'errors': loader.plugin_errors
        })
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


def execute_plugin_js(plugin_id: str, nodes_json: str, edges_json: str, parameters_json: str = "{}") -> str:
    """JavaScript interface: Execute plugin and return results as JSON"""
    try:
        loader = get_plugin_loader()
        
        # Parse JSON inputs
        nodes = json.loads(nodes_json)
        edges = json.loads(edges_json)
        parameters = json.loads(parameters_json)
        
        # Execute plugin
        results = loader.execute_plugin(plugin_id, nodes, edges, parameters)
        
        return json.dumps({
            'success': True,
            'results': results
        })
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })