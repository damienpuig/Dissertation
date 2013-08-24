import os, sys
import glob
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
sys.path.append(os.path.join(os.path.dirname(__file__), '..\..\..\..\Representation'))
print sys.path