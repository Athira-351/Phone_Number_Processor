import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PreviewFile = ({ filename }) => {
    const [previewData, setPreviewData] = useState([]);

    useEffect(() => {
        const fetchPreview = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/preview/${filename}`);
                setPreviewData(response.data);
            } catch (error) {
                console.error('Error fetching preview:', error);
            }
        };
        if (filename) fetchPreview();
    }, [filename]);

    return (
        <div>
            <h4 className="mt-4">File Preview:</h4>
            {previewData.length > 0 ? (
                <table className="table table-bordered table-hover mt-3">
                    <thead className="thead-light">
                        <tr>
                            {Object.keys(previewData[0]).map((key) => (
                                <th key={key}>{key}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {previewData.map((row, index) => (
                            <tr key={index}>
                                {Object.values(row).map((val, idx) => (
                                    <td key={idx}>{val}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p className="text-muted mt-2">No preview available.</p>
            )}
        </div>
    );
};

export default PreviewFile;
