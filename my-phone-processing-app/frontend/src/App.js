import React, { useState } from 'react';
import UploadFile from './components/UploadFile';
import PreviewFile from './components/PreviewFile';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import { FiHelpCircle } from 'react-icons/fi';

const App = () => {
    const [uploadedFile, setUploadedFile] = useState(null);
    const [showHelp, setShowHelp] = useState(false);

    // Toggle help message box visibility
    const toggleHelpBox = () => {
        setShowHelp(!showHelp);
    };

    return (
        <div className="container mt-5">
            <h2 className="title text-center">Phone Number Formatter</h2>
            <br />
            <UploadFile onFileUpload={setUploadedFile} />
            {uploadedFile && (
                <>
                    <PreviewFile filename={uploadedFile} />
                    <div className="text-center mt-3">
                        <a href={`http://localhost:5000/download/${uploadedFile}`} className="btn btn-success" download>
                            Download Processed File
                        </a>
                    </div>
                </>
            )}

            {/* Help Icon at bottom right */}
            <div className="help-icon" onClick={toggleHelpBox}>
                <FiHelpCircle size={40} />
            </div>

            {/* Help message box */}
            {showHelp && (
                <div className="help-box">
                    <p>
                        If you encounter any issues with preview or download, please rename your column to 'Phone_Number', 'Mobile_Number', 'phone number', 'mobile number', 'Number', 'number', 'num', 'Num', 'mobile', or 'Phone' to resolve compatibility problems.
                    </p>
                </div>
            )}

        </div>
    );
};

export default App;
