from agent_5b_generator import RunwayImageGenerator

try:
    generator = RunwayImageGenerator()
    print("✅ Agent 5b: Import successful!")
    print(f"✅ Output directory: {generator.output_dir}")
except Exception as e:
    print(f"❌ Error: {e}")
