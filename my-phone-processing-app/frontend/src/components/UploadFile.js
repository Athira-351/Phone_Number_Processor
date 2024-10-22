import React, { useState } from 'react';
import axios from 'axios';
import PreviewFile from './PreviewFile';  
import '../index.css';

const UploadFile = ({ onFileUpload }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadedFile, setUploadedFile] = useState(null); 

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file to upload.');
            return;
        }
        const formData = new FormData();
        formData.append('file', selectedFile);
    
        try {
            const response = await axios.post('http://localhost:5000/upload', formData);
            setUploadedFile(response.data.file); // Update local state with uploaded file
            onFileUpload(response.data.file); // Call parent function
            alert('File uploaded and processed successfully');
        } catch (error) {
            const errorMessage = error.response ? error.response.data.error : 'Error uploading file';
            alert(errorMessage);
        }
    };

    return (
        <div className="upload-section text-center mt-4">
            <input type="file" className="form-control-file mb-3" onChange={handleFileChange} />
            <button className="btn btn-primary mr-2" onClick={handleUpload}>Upload</button>
            <button className="btn btn-secondary" onClick={() => setSelectedFile(null)}>Cancel</button>
            {uploadedFile && <PreviewFile filename={uploadedFile} />}
        </div>
    );
};

export default UploadFile;
