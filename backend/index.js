const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage for plants (in production, you'd use a database)
let plants = [
  {
    id: 1,
    name: 'Snake Plant',
    species: 'Sansevieria trifasciata',
    careLevel: 'Easy',
    wateringFrequency: 'Every 2-3 weeks',
    sunlight: 'Low to bright indirect light',
    description: 'A hardy plant that can survive neglect and purify air.',
    lastWatered: new Date().toISOString().split('T')[0]
  },
  {
    id: 2,
    name: 'Pothos',
    species: 'Epipremnum aureum',
    careLevel: 'Easy',
    wateringFrequency: 'When top inch of soil is dry',
    sunlight: 'Low to bright indirect light',
    description: 'A trailing vine that\'s perfect for beginners.',
    lastWatered: new Date().toISOString().split('T')[0]
  }
];

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Plant Care API is running!' });
});

// Get all plants
app.get('/api/plants', (req, res) => {
  res.json(plants);
});

// Get single plant
app.get('/api/plants/:id', (req, res) => {
  const plant = plants.find(p => p.id === parseInt(req.params.id));
  if (!plant) {
    return res.status(404).json({ message: 'Plant not found' });
  }
  res.json(plant);
});

// Add new plant
app.post('/api/plants', (req, res) => {
  const newPlant = {
    id: plants.length + 1,
    name: req.body.name,
    species: req.body.species || '',
    careLevel: req.body.careLevel || 'Medium',
    wateringFrequency: req.body.wateringFrequency || 'Weekly',
    sunlight: req.body.sunlight || 'Medium indirect light',
    description: req.body.description || '',
    lastWatered: req.body.lastWatered || new Date().toISOString().split('T')[0]
  };

  plants.push(newPlant);
  res.status(201).json(newPlant);
});

// Update plant
app.put('/api/plants/:id', (req, res) => {
  const plant = plants.find(p => p.id === parseInt(req.params.id));
  if (!plant) {
    return res.status(404).json({ message: 'Plant not found' });
  }

  Object.keys(req.body).forEach(key => {
    if (req.body[key] !== undefined) {
      plant[key] = req.body[key];
    }
  });

  res.json(plant);
});

// Delete plant
app.delete('/api/plants/:id', (req, res) => {
  const plantIndex = plants.findIndex(p => p.id === parseInt(req.params.id));
  if (plantIndex === -1) {
    return res.status(404).json({ message: 'Plant not found' });
  }

  plants.splice(plantIndex, 1);
  res.json({ message: 'Plant deleted successfully' });
});

// Mark plant as watered
app.patch('/api/plants/:id/water', (req, res) => {
  const plant = plants.find(p => p.id === parseInt(req.params.id));
  if (!plant) {
    return res.status(404).json({ message: 'Plant not found' });
  }

  plant.lastWatered = new Date().toISOString().split('T')[0];
  res.json(plant);
});

app.listen(PORT, () => {
  console.log(`Plant Care API server is running on port ${PORT}`);
});
