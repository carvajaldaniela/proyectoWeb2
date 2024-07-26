import React, { useState } from 'react';
import axios from 'axios';

const TaxpayerForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    id_number: '',
    address: '',
    email: '',
    digital_signature: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/contribuyentes', formData)
      .then(response => {
        alert('Contribuyente registrado exitosamente');
      })
      .catch(error => {
        console.error('Hubo un error registrando al contribuyente', error);
        alert('Error al registrar contribuyente');
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Nombre:
        <input type="text" name="name" value={formData.name} onChange={handleChange} required />
      </label>
      <br />
      <label>
        Tipo:
        <input type="text" name="type" value={formData.type} onChange={handleChange} required />
      </label>
      <br />
      <label>
        Número de Identificación:
        <input type="text" name="id_number" value={formData.id_number} onChange={handleChange} required />
      </label>
      <br />
      <label>
        Dirección:
        <input type="text" name="address" value={formData.address} onChange={handleChange} required />
      </label>
      <br />
      <label>
        Correo Electrónico:
        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
      </label>
      <br />
      <label>
        Firma Digital:
        <input type="text" name="digital_signature" value={formData.digital_signature} onChange={handleChange} required />
      </label>
      <br />
      <button type="submit">Registrar Contribuyente</button>
    </form>
  );
};

export default TaxpayerForm;
