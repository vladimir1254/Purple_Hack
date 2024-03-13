import React, { useState } from 'react';
import './App.css'; // Импортируем файл со стилями
import FileUploadComponent from './components/FileUploadComponent';

function App() {
  const [locationId, setLocationId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [price, setPrice] = useState('');
  const [errorFields, setErrorFields] = useState([]);
  const request_ap = 'http://localhost:8000'

 // const request_ap = 'http://194.163.137.219:8000'
  
  const checkEmptyFields = () => {
    let fieldsWithError = [];
    if (!locationId) {
      fieldsWithError.push('locationId');
    }
    if (!categoryId) {
      fieldsWithError.push('categoryId');
    }
    if (!price) {
      fieldsWithError.push('price');
    }
    return fieldsWithError;
  };

  const handleLocationIdChange = (event) => {
    setLocationId(event.target.value);
    if (errorFields.includes('locationId')) {
      setErrorFields(errorFields.filter(field => field !== 'locationId'));
    }
  };

  const handleCategoryIdChange = (event) => {
    setCategoryId(event.target.value);
    if (errorFields.includes('categoryId')) {
      setErrorFields(errorFields.filter(field => field !== 'categoryId'));
    }
  };

  const handlePriceChange = (event) => {
    setPrice(event.target.value);
    if (errorFields.includes('price')) {
      setErrorFields(errorFields.filter(field => field !== 'price'));
    }
  };


  const handleUpdateClick = () => {
    const fieldsWithError = checkEmptyFields();
    setErrorFields(fieldsWithError);
  
    if (fieldsWithError.length > 0) {
      return;
    }

    // Отправляем запрос на обновление
    fetch(`${request_ap}/ui/update_price?location_id=${locationId}&category_id=${categoryId}&price=${price}`)
      .then(response => {
        // Обрабатываем ответ
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  };

  const handleInsertClick = () => {
    const fieldsWithError = checkEmptyFields();
    setErrorFields(fieldsWithError);
  
    if (fieldsWithError.length > 0) {
      return;
    }

    // Отправляем запрос на вставку
    fetch(`${request_ap}/ui/add_price`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location_id: locationId,
        category_id: categoryId,
        price: price,
      }),
    })
      .then(response => {
        console.log(response)
        // Обрабатываем ответ
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  };

  const handleDeleteClick = () => {
    const fieldsWithError = checkEmptyFields().filter(field => field !== 'price'); // Исключаем проверку цены для кнопки удаления
    setErrorFields(fieldsWithError);
  
    if (fieldsWithError.length > 0) {
      return;
    }

    // Отправляем запрос на удаление
    fetch(`${request_ap}/ui/delete_price`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location_id: locationId,
        category_id: categoryId,
        price: price,
      }),
    })
      .then(response => {
        console.log('success delete')
        // Обрабатываем ответ
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  };


  return (
    <div className="container">
  <div className="new-prices-section">
    <h2>New prices</h2>
    <div className="input-buttons-wrapper">
      <div className="input-wrapper">
        <label htmlFor="locationId">Location ID:</label>
        <input
          type="text"
          id="locationId"
          value={locationId}
          onChange={handleLocationIdChange}
          placeholder="Enter Location ID"
          className={`input ${errorFields.includes('locationId') ? 'error' : ''}`}
        />
      </div>
      <div className="input-wrapper">
        <label htmlFor="categoryId">Category ID: </label>
        <input
          type="text"
          id="categoryId"
          value={categoryId}
          onChange={handleCategoryIdChange}
          placeholder="Enter Category ID"
          className={`input ${errorFields.includes('categoryId') ? 'error' : ''}`}
        />
      </div>
      <div className="input-wrapper">
        <label htmlFor="price">Price: </label>
        <input
          type="text"
          id="price"
          value={price}
          onChange={handlePriceChange}
          placeholder="Enter Price"
          className={`input ${errorFields.includes('price') ? 'error' : ''}`}
        />
      </div>
    </div>
        <button onClick={handleInsertClick} className="button">Add price</button>
          <button onClick={handleInsertClick} className="button">Update price</button>
          <button onClick={handleDeleteClick} className="button">Delete price</button>
      </div>
      <div className="matrix-upload-section">
        <h2>MATRIX UPLOAD</h2>
        <div className="file-upload-container">
          <div className="file-upload-component-wrapper">
            <FileUploadComponent matrix={'baseline'} request_ap={request_ap} />
          </div>
          <div className="file-upload-component-wrapper">
            <FileUploadComponent matrix={'discount'} request_ap={request_ap} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;