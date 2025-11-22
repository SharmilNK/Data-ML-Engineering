"""
Docker Entry Point - Handles different commands
"""
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: python entrypoint.py [train|serve|predict]")
        print("")
        print("Commands:")
        print("  train  - Run the ML training pipeline")
        print("  serve  - Start the FastAPI server")
        print("  predict - Make a prediction (requires additional args)")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "train":
        print("=" * 60)
        print("STARTING TRAINING PIPELINE")
        print("=" * 60)
        from main import run_pipeline
        run_pipeline()
    
    elif command == "serve":
        print("=" * 60)
        print("STARTING API SERVER")
        print("=" * 60)
        import uvicorn
        uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=False)
    
    elif command == "predict":
        if len(sys.argv) < 4:
            print("Usage: python entrypoint.py predict <date> <borough>")
            print("Example: python entrypoint.py predict 2024-06-15 bronx")
            sys.exit(1)
        
        date = sys.argv[2]
        borough = sys.argv[3]
        
        print(f"Predicting for {date} in {borough}...")
        # We'll implement this in Step 6
        print("Prediction endpoint not yet implemented. Use 'serve' and call API.")
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: train, serve, predict")
        sys.exit(1)


if __name__ == "__main__":
    main()
