import sys
import os
import runpy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'h-lang'))

# Run the parser module directly as __main__ to test it
print("Testing parser by running it as main module...")
runpy.run_module('core.parser', run_name='__main__')
