


# End-to-End Source Code Analysis with Generative AI

A comprehensive solution for analyzing and processing source code using generative AI models. This project leverages the power of OpenAI's models to provide insightful analysis on various aspects of source code.

---

## Getting Started

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) (for managing environments)
- An OpenAI API key (for accessing AI capabilities)

### Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/PriyanshuDey23/Source-Code-Analysis-Generative-AI.git

```

#### Step 2: Create a Conda Environment

```bash
conda create -n llmapp python=3.10 -y
conda activate llmapp
```

#### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

#### Step 4: Set Up API Credentials

Create a `.env` file in the project root directory and add your OpenAI API key:

```ini
GOOGLE_API_KEY="your_google_api_key_here"
```

#### Step 5: Run the Application

Start the app with the following command:

```bash
python app.py
```

#### Step 6: Access the Application

Open your browser and navigate to `http://localhost:5000` to start using the application.

---

## Tech Stack

- **Python**: Core language for the project
- **LangChain**: Framework for interacting with language models
- **Flask**: Web application framework
- **Google Gemini**: AI model for code analysis
- **ChromaDB**: Database for storing and retrieving embeddings

---

Feel free to contribute to this project by submitting issues, feature requests, or pull requests!
