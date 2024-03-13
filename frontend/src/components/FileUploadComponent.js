import React, { useState } from 'react';
import axios from 'axios';
import '../App.css'; // Импортируем файл со стилями
import JSZip from 'jszip';


const FileUploadComponent = ({matrix,request_ap}) => {
  console.log(matrix)
  const [selectedFile, setSelectedFile] = useState(null);

  // Обработчик изменения файла
  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    // Проверяем расширение файла
    const allowedExtensions = ["zip"];
    const extension = file.name.split('.').pop().toLowerCase();
  
    if (!allowedExtensions.includes(extension)) {
      // Если расширение файла не соответствует .zip, то архивируем его
    // Создаем новый экземпляр JSZip
    const zip = new JSZip();
    const folder = zip.folder("files");
    await folder.file(file.name, file);

    // Генерируем архив с сжатием Deflate
    const content = await zip.generateAsync({ type: "blob", compression: "DEFLATE" });

    // Создаем новый файл с архивом
    const zipFile = new File([content], file.name + '.zip', { type: "application/zip" });

      setSelectedFile(zipFile);

      // Отправляем архив на сервер
      // Ваша логика отправки файла на сервер
    } else {
      setSelectedFile(event.target.files[0]);

      // Если файл уже является архивом, просто отправляем его на сервер
      // Ваша логика отправки файла на сервер
    }

  };

  // Обработчик отправки файла на сервер
  const handleUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('matrix', matrix);
      formData.append('file', selectedFile);
      console.log('FormData=',formData)
      axios.post(`${request_ap}/upload`, formData)
        .then((response) => {
          console.log('File uploaded successfully');
          // Добавьте здесь логику для обработки ответа сервера после успешной загрузки файла
        })
        .catch((error) => {
          console.error('Error uploading file:', error);
        });
    }
  };

  return (
<div>
  <div className="file-upload-container">
    <input className="file-input" type="file" onChange={handleFileChange} />
  </div>
  <div className="button-container">
    <button className="button" onClick={handleUpload}>
    {matrix === 'baseline' ? 'Download baseline matrix' : 'Download discount matrix'}
    </button>
  </div>
</div>
  );
};

export default FileUploadComponent;