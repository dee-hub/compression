import streamlit as st
import os
import tfci
import subprocess
import tempfile
def compress_image(image_path, algorithm, quality):
    if algorithm == "Factorized Prior Autoencoder":
        subprocess.run(["python", "tfci.py", "compress", f"bmshj2018-factorized-msssim-{quality}", image_path])
        return image_path + ".tfci"
    elif algorithm == "Nonlinear transform coder model with factorized priors":
        subprocess.run(["python", "tfci.py", "compress", "b2018-gdn-128-1", image_path])
        return image_path + ".tfci"
    # Add logic for the third algorithm

def decompress_image(image_path, algorithm):
    decompressed_path = image_path.replace(".tfci", "_decompressed.jpg")
    subprocess.run(["python", "tfci.py", "decompress", image_path, decompressed_path])
    return decompressed_path

def main():
    st.title("Image Compression & Decompression App")

    operation = st.selectbox("Choose Operation", ["Compress", "Decompress"])

    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        algorithm = st.selectbox("Choose Compression Algorithm", [
            "Factorized Prior Autoencoder", 
            "Nonlinear Transform Coder Model with Factorized Priors", 
            "Hyperprior Model with Non Zero-Mean Gaussian Conditionals"
        ])

        if algorithm == "Factorized Prior Autoencoder":
            quality = st.selectbox("Select a quality level", [1, 2, 3, 4, 5, 6, 7, 8])
        elif algorithm == "Nonlinear Transform Coder Model with Factorized Priors":
            quality = st.selectbox("Select a quality level", [1, 2, 3, 4])
        elif algorithm == "Hyperprior Model with Non Zero-Mean Gaussian Conditionals":
            quality = st.selectbox("Select a quality level", [1, 2, 3, 4, 5, 6, 7, 8])
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")  # you can adjust the suffix based on the uploaded file type
        temp_file.write(uploaded_image.read())
        
        if st.button("Execute"):
            if operation == "Compress":
                # Call the function to compress
                compressed_file = compress_image(temp_file.name, algorithm, quality)
                st.write("Compression Done!")
                st.download_button('Download Compressed File', compressed_file)
                #with open(compressed_file, 'rb') as f:
                    #st.download_button('Download Compressed File', f, file_name=compressed_file)
                    #st.download_button(label="", data=compressed_file)

            else:
                # Call the function to decompress
                decompressed_file = decompress_image(uploaded_image, algorithm)
                st.write("Decompression Done!")
                st.download_button(label="Download Decompressed File", data=decompressed_file)

if __name__ == "__main__":
    main()
