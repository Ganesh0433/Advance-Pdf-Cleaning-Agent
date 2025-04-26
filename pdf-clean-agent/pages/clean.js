"use client";

import { useState } from "react";
import axios from "axios";

export default function CleanPDF() {
  const [pdfFile, setPdfFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setPdfFile(file);
    setSuccess(false);
    setError(null);
    if (file && file.type === "application/pdf") {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    if (!pdfFile) {
      setError("Please select a PDF file");
      setIsLoading(false);
      return;
    }

    if (!prompt.trim()) {
      setError("Please enter cleaning instructions");
      setIsLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", pdfFile);
      formData.append("prompt", prompt);

      const response = await axios.post(
        "https://advance-pdf-cleaning-agent.onrender.com/clean-pdf",
        formData,
        {
          responseType: "blob",
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.error || "Error processing PDF");
      console.error("Error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <style jsx>{`
        :root {
          --navy-600: #1e3a8a;
          --navy-700: #1e2f6d;
          --navy-900: #172554;
          --teal-50: #e6fffa;
          --teal-600: #0d9488;
          --teal-700: #0b8276;
        }
        .bg-navy-600 { background-color: var(--navy-600); }
        .bg-navy-700 { background-color: var(--navy-700); }
        .text-navy-900 { color: var(--navy-900); }
        .bg-teal-50 { background-color: var(--teal-50); }
        .bg-teal-600 { background-color: var(--teal-600); }
        .bg-teal-700 { background-color: var(--teal-700); }
        .focus\\:ring-navy-500:focus { --tw-ring-color: var(--navy-600); }
        .focus\\:ring-teal-500:focus { --tw-ring-color: var(--teal-600); }
        .hover\\:bg-navy-700:hover { background-color: var(--navy-700); }
        .hover\\:bg-teal-700:hover { background-color: var(--teal-700); }
      `}</style>
      <div className="min-h-screen bg-gray-100 flex flex-col p-6 font-sans">
        <div className="flex-1 w-full max-w-6xl mx-auto bg-white rounded-xl shadow-lg p-8">
          <header className="text-center mb-8">
            <h1 className="text-3xl font-bold text-navy-900">PDF Cleaner</h1>
            <p className="mt-2 text-sm text-gray-600">
              Securely clean your PDF documents
            </p>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <section className="space-y-6">
              <div>
                <label
                  htmlFor="pdf-upload"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Upload PDF
                </label>
                <div className="flex items-center">
                  <label
                    htmlFor="pdf-upload"
                    className="cursor-pointer bg-navy-600 text-white py-2 px-4 rounded-md hover:bg-navy-700 focus:outline-none focus:ring-2 focus:ring-navy-500 focus:ring-offset-2 transition"
                  >
                    Select File
                    <input
                      id="pdf-upload"
                      type="file"
                      accept=".pdf"
                      onChange={handleFileChange}
                      className="hidden"
                      aria-describedby="pdf-upload-help"
                    />
                  </label>
                  <span className="ml-3 text-sm text-gray-600 truncate max-w-xs">
                    {pdfFile ? pdfFile.name : "No file selected"}
                  </span>
                </div>
                <p id="pdf-upload-help" className="mt-1 text-xs text-gray-500">
                  Only PDF files are supported
                </p>
              </div>

              <div>
                <label
                  htmlFor="instructions"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Cleaning Instructions
                </label>
                <textarea
                  id="instructions"
                  rows={4}
                  className="w-full border border-gray-200 rounded-md p-3 focus:ring-2 focus:ring-navy-500 focus:border-navy-500 transition"
                  placeholder="E.g., Remove personal information, headers, or footers"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  aria-describedby="instructions-help"
                />
                <p id="instructions-help" className="mt-1 text-xs text-gray-500">
                  Specify what to remove from the PDF
                </p>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={handleSubmit}
                  disabled={isLoading}
                  className={`flex-1 py-2.5 rounded-md text-white font-medium ${
                    isLoading
                      ? "bg-gray-400 cursor-not-allowed"
                      : "bg-navy-600 hover:bg-navy-700"
                  } flex items-center justify-center transition focus:outline-none focus:ring-2 focus:ring-navy-500 focus:ring-offset-2`}
                  aria-busy={isLoading}
                >
                  {isLoading ? (
                    <>
                      <svg
                        className="animate-spin h-5 w-5 mr-2 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      Processing
                    </>
                  ) : (
                    "Clean PDF"
                  )}
                </button>

                {success && (
                  <a
                    href={downloadUrl}
                    download="cleaned.pdf"
                    className="flex-1 py-2.5 rounded-md bg-teal-600 text-white font-medium hover:bg-teal-700 text-center transition focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
                    aria-label="Download cleaned PDF"
                  >
                    Download
                  </a>
                )}
              </div>

              {(error || success) && (
                <div
                  className={`p-3 rounded-md transition-opacity duration-300 ${
                    error ? "bg-red-50 text-red-700" : "bg-teal-50 text-teal-700"
                  }`}
                  role="alert"
                >
                  <p className="text-sm">
                    {error || "PDF cleaned successfully"}
                  </p>
                </div>
              )}
            </section>

            {previewUrl && (
              <section
                className="bg-gray-50 rounded-lg p-6"
                aria-label="PDF preview"
              >
                <h2 className="text-sm font-medium text-gray-700 mb-3">
                  Document Preview
                </h2>
                <iframe
                  src={previewUrl}
                  className="w-full h-[650px] rounded-md border border-gray-200"
                  title="PDF Preview"
                  aria-describedby="pdf-preview"
                />
              </section>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
