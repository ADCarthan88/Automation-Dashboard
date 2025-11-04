import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import apiClient from '../utils/api';

function EmailParser() {
  const navigate = useNavigate();
  const [emailContent, setEmailContent] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleParse = async () => {
    if (!emailContent.trim()) {
      setError('Please enter email content');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/tasks/email-parse', {
        task_type: 'email_parse',
        parameters: {
          email_content: emailContent
        }
      });

      setResult(response.data.result);
    } catch (err) {
      setError('Failed to parse email: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Button onClick={() => navigate('/')} sx={{ mb: 2 }}>
        ← Back to Dashboard
      </Button>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Email Parser
        </Typography>

        <TextField
          fullWidth
          multiline
          rows={10}
          label="Email Content"
          placeholder="Paste your email content here..."
          value={emailContent}
          onChange={(e) => setEmailContent(e.target.value)}
          sx={{ mb: 3 }}
        />

        <Button
          variant="contained"
          onClick={handleParse}
          disabled={loading}
          sx={{ mb: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Parse Email'}
        </Button>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Parsed Results:
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

export default EmailParser;