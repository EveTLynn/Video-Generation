# Video Generation App

This app generates videos based on an image and text prompt input using **FastAPI** for the backend and **Streamlit** for the frontend. The video generation model, **I2VGenXLPipeline**, is hosted on Google Colab.

## Features

- Upload an image and provide a text prompt.
- Generates a downloadable video based on the input.

## Tech Stack

- **Backend**: FastAPI, I2VGenXLPipeline (hosted on Colab).
- **Frontend**: Streamlit.

## Requirements

### Backend (FastAPI + Colab)

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn torch transformers i2vgenxl opencv-python pillow aiofiles
   ```
2. Run FastAPI server:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
3. Expose the backend via `ngrok` or a similar service (if on Colab).

### Frontend (Streamlit)

1. Install Streamlit and requests:
   ```bash
   pip install streamlit requests
   ```
2. Start the frontend:
   ```bash
   streamlit run app.py
   ```

## Example

- **Image**: Landscape photo.
- **Prompt**: "Time-lapse of a sunset over mountains."
- **Output**: Short video depicting a sunset over mountains.

## File Structure

```
├── backend
│   ├── app.py                  # FastAPI app
│   ├── i2vgen_pipeline.ipynb   # Model pipeline (Colab)
├── frontend
│   ├── app.py                  # Streamlit app
└── README.md                   # Documentation
```

## License

Licensed under the MIT License.
