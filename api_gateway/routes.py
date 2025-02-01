from fastapi import HTTPException,FastAPI
import sys,uvicorn
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.database import initialize_db
from model.database import fetch_all_packets, clear_packets


initialize_db()

class setup_routes:
    def __init__(self):
        self.app= FastAPI(
            title="Network Analysis API Gateway",
            description="Manages packet captures, analysis, and client-server communication",
            version="1.0.0",
            )
        self.set_api()


# Include the router
    def set_api(self):
        # Health check
        @self.app.get("/health")
        def health_check():
            
            return {"status": "ok", "message": "API Gateway is running"}



        @self.app.get("/packets")
        def get_packets():
            packets = fetch_all_packets()
            if not packets:
                return {"message": "No packets found in the database.", "packets": []}
            return {"packets": packets}

        @self.app.delete("/clear_packets")
        def clear_all_packets():
            try:
                clear_packets()
                return {"message": "All packets cleared successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to clear packets: {str(e)}")

    def run_server(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    
    
    initialize_db()
    setup_routes().run_server()
    
    