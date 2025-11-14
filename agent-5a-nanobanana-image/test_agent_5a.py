from agent_5a_generator import NanobananaImageGenerator

try:
    generator = NanobananaImageGenerator()
    print("✅ Agent 5a: Import successful!")
    print(f"✅ Output directory: {generator.output_dir}")
except Exception as e:
    print(f"❌ Error: {e}")
