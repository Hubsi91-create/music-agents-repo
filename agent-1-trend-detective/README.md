Music Inspiration Generator Agent

A production-ready AI agent built with Google Cloud Vertex AI Agent Development Kit (ADK) that generates creative song concepts with lyrics, genre recommendations, and mood descriptions.



🎵 Features

Creative Song Concepts: Generates 2-3 unique song ideas per request



Sample Lyrics: Provides verse, chorus, and bridge lyrics



Genre Recommendations: Suggests primary genres, subgenres, and fusion styles



Mood Descriptions: Rich, evocative emotional and atmospheric guidance



Technical Specifications: BPM, key signature, instrumentation



Production Notes: Actionable production and arrangement advice



JSON Output: Structured, machine-readable responses



🚀 Quick Start

Prerequisites

Google Cloud Project with billing enabled



Vertex AI API enabled



Python 3.9-3.12



Google Cloud SDK (gcloud CLI)



Installation

bash

\# Clone or download this agent directory

cd music-inspiration-generator



\# Install dependencies

make install



\# Initialize environment variables

make init

Local Testing

bash

\# Run interactive playground

make playground



\# Or test directly

make test

Deployment

bash

\# Deploy to Vertex AI Agent Engine

make deploy

📁 Project Structure

text

music-inspiration-generator/

├── agent.py

├── system\_prompt.txt

├── requirements.txt

├── Makefile

├── README.md

└── .env

🔧 Configuration

Edit these values in the Makefile or set as environment variables.



💡 Usage Examples

See agent.py for Python usage examples.



📊 Response Format

See agent.py and system\_prompt.txt for output format.



🛠️ Makefile Commands

Command	Description

make help	Show all available commands

make install	Install Python dependencies

make init	Create .env configuration file

make setup-bucket	Create GCS staging bucket

make playground	Run interactive ADK playground

make test	Test agent locally

make deploy	Deploy to Vertex AI Agent Engine

make clean	Remove temporary files

🧪 Testing

After deployment, test your agent via Vertex AI Console, API endpoint, or Python SDK.



🔐 Authentication

Application Default Credentials (ADC) required.



📝 Model Information

Gemini 2.5 Pro, Vertex AI, us-central1



🎯 Use Cases

Music production, songwriting, genre exploration, creative brainstorming



🐛 Troubleshooting

See README for error resolution, authentication, and deployment help.



📚 Additional Resources

ADK Documentation



Vertex AI Agent Engine



Gemini 2.5 Pro



📄 License

Provided as-is for educational and production use.



🤝 Contributing

Contributions welcome! Please test thoroughly before submitting changes.

