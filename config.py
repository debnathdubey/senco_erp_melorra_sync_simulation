import os

# Default configuration for Acxiom - Senco ERP Melorra Sync Simulation
DEFAULT_API_KEY = os.getenv("X_API_KEY", "Acxiom-Melorra-Secret-Key-2026")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "9000"))
