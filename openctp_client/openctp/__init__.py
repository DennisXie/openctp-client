try:
    from openctp_ctp import tdapi
    from openctp_ctp import mdapi
except ImportError:
    from openctp_tts import tdapi
    from openctp_tts import mdapi

# The following code is more useful, but it is not friendly to intelligent code completion.
# 
# import sys
# import importlib.util
#
# packages = ["openctp_ctp", "openctp_tts"]
# tdapi = None
# mdapi = None
# 
# for package in packages:
#     spec = importlib.util.find_spec(package)
#     if spec is not None:
#         module = importlib.util.module_from_spec(spec)
#         sys.modules[package] = module
#         spec.loader.exec_module(module)
#         tdapi = module.tdapi
#         mdapi = module.mdapi
#         break
