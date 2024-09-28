
import streamlit as st
import requests
import uuid
import base64

# Set page configuration
st.set_page_config(layout="wide", page_title="Multimodal Video Generator", page_icon="🎥")
st.title("Multimodal Video Generator 🎥")

# print(st.session_state)

# Generate a random session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  

# Initialize the session state for the backend URL
if "api_url" not in st.session_state:
    st.session_state.api_url = None

# Function to display the dialog and set the URL
@st.dialog("Setup Backend")
def setup_backend():
    st.markdown(
        """
        Run the backend [here](https://colab.research.google.com/drive/12fgJ3r8L73hfjKfNnIV2RAtEJvf9qwZf?usp=sharing) 
        and paste the Ngrok link below.
        """
    )
    link = st.text_input("Backend URL", "")
    if st.button("Save"):
        st.session_state.api_url = link
        st.session_state.generate_api_url = "{}/generate-video".format(link)  
        st.session_state.upload_api_url = "{}/upload-image".format(link)
        st.rerun()  # Re-run the app to close the dialog

# Display the setup option if the URL is not set
if not st.session_state.api_url:
    st.warning("Backend URL is not set! Please set up the backend.")
    setup_backend()

# Once the URL is set, display it 
if st.session_state.api_url:
    st.success(f"Backend is set to: {st.session_state.generate_api_url}", icon="✅")

# Separate input for image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, width=400)
    
    # Convert file-like object to bytes and send to the backend
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(st.session_state.upload_api_url, files=files)
    
    # Display the response from the server
    if response.status_code == 200:
        st.success(f"File successfully uploaded: {response.json()['filename']}")
    else:
        st.error("Failed to upload file.")

# Function to call FastAPI and get the video
def get_video_from_api(prompt: str, negative_prompt: str, 
                       seed: int, num_inference_steps: int, 
                       guidance_scale: float, num_frames: int, 
                       target_fps: int, image_filename: str):
    
    payload = {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'seed': seed,  
        'num_inference_steps': num_inference_steps,  
        'guidance_scale': guidance_scale,
        'num_frames': num_frames,
        'fps': target_fps,
        'image_filename': image_filename
    }

    # POST request to FastAPI server
    response = requests.post(st.session_state.generate_api_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return response.content  # The video content (MP4)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None
    

# Input section for video prompt
with st.container():
    st.header("Generate Your Video")
    
    # Tabbed layout for prompt and settings
    tab1, tab2 = st.tabs(["Prompt", "Settings"])

    with tab1:
        prompt = st.text_area("Enter the prompt for the video:", 
                              "A cat is shivering and covered in snow from a raging blizzard.")
        negative_prompt = st.text_input("Enter negative prompt:", 
                                        "Distorted, discontinuous, ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, incomplete arms")

    with tab2:
        st.write("#### Video Settings")
        num_frames = st.slider("Number of frames:", min_value=1, max_value=100, value=30, step=1)
        fps = st.slider("FPS (frames per second):", min_value=1, max_value=60, value=5, step=1)
        guidance_scale = st.slider("Guidance Scale", min_value=5.0, max_value=15.0, value=9.0, step=0.1)
        seed = st.number_input("Seed", value=8888)
        num_inference_steps = st.number_input("Inference Steps", min_value=1, max_value=500, value=50, step=1)
        

button = st.button("Generate Video")

# Process inputs only if both are provided
if prompt and uploaded_file and button:
    with st.spinner("Generating video..."):
        # Call the API to generate the video
        video_content = get_video_from_api(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            num_frames=num_frames,
            target_fps=fps,
            image_filename=uploaded_file.name
        )
        # print(st.session_state)
        # If video is generated, display it
        if video_content:
            # Save the video to a temporary file
            video_path = "generated_video.mp4"
            with open(video_path, "wb") as video_file:
                video_file.write(video_content)

            video_file = open("generated_video.mp4", "rb")
            video_bytes = video_file.read()
            # Convert video bytes to base64
            video_base64 = base64.b64encode(video_bytes).decode('utf-8')

            # Display the video with custom width, height, and centered using HTML and CSS
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <video width="800" height="400" controls>
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Download button
            st.download_button("Download Video", data=video_bytes, file_name="generated_video.mp4")
