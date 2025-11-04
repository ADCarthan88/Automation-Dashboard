import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Grid
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import apiClient from '../utils/api';

function InvoiceGenerator() {
  const navigate = useNavigate();
  const [clientInfo, setClientInfo] = useState({
    name: '',
    email: '',
    address: ''
  });
  const [items, setItems] = useState([
    { description: '', quantity: 1, price: 0 }
  ]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!clientInfo.name.trim()) {
      setError('Please enter client name');
      return;
    }

    const validItems = items.filter(item => 
      item.description.trim() && item.quantity > 0 && item.price >= 0
    );

    if (validItems.length === 0) {
      setError('Please add at least one valid item');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await apiClient.post('/tasks/invoice-generate', {
        task_type: 'invoice_generate',
        parameters: {
          client_info: clientInfo,
          items: validItems
        }
      });

      if (response.data && response.data.result) {
        setResult(response.data.result);
      } else {
        setError('Invalid response from server');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.error || 
                          err.message || 
                          'An unexpected error occurred';
      setError('Failed to generate invoice: ' + errorMessage);
      console.error('Invoice generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const addItem = () => {
    setItems([...items, { description: '', quantity: 1, price: 0 }]);
  };

  const updateItem = (index, field, value) => {
    if (index < 0 || index >= items.length) {
      console.error('Invalid item index:', index);
      return;
    }
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  };

  const removeItem = (index) => {
    if (items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Button onClick={() => navigate('/')} sx={{ mb: 2 }}>
        ← Back to Dashboard
      </Button>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Invoice Generator
        </Typography>

        <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
          Client Information
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Client Name"
              placeholder="Enter client name"
              required
              value={clientInfo.name}
              onChange={(e) => setClientInfo({...clientInfo, name: e.target.value})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Email Address"
              placeholder="client@example.com"
              type="email"
              value={clientInfo.email}
              onChange={(e) => setClientInfo({...clientInfo, email: e.target.value})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Billing Address"
              placeholder="123 Main St, City, State 12345"
              value={clientInfo.address}
              onChange={(e) => setClientInfo({...clientInfo, address: e.target.value})}
            />
          </Grid>
        </Grid>

        <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
          Items
        </Typography>
        {items.map((item, index) => (
          <Grid container spacing={2} key={index} sx={{ mb: 2 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Item Description"
                placeholder="Service or product description"
                required
                value={item.description}
                onChange={(e) => updateItem(index, 'description', e.target.value)}
              />
            </Grid>
            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="Quantity"
                type="number"
                inputProps={{ min: 1 }}
                value={item.quantity}
                onChange={(e) => updateItem(index, 'quantity', Math.max(1, parseInt(e.target.value) || 1))}
              />
            </Grid>
            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="Unit Price ($)"
                type="number"
                inputProps={{ min: 0, step: 0.01 }}
                value={item.price}
                onChange={(e) => updateItem(index, 'price', Math.max(0, parseFloat(e.target.value) || 0))}
              />
            </Grid>
          </Grid>
        ))}

        <Button onClick={addItem} sx={{ mb: 3 }}>
          Add Item
        </Button>

        <Box>
          <Button
            variant="contained"
            onClick={handleGenerate}
            disabled={loading}
            sx={{ mb: 3 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Invoice'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Generated Invoice:
            </Typography>
            <Paper sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </Paper>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default InvoiceGenerator;