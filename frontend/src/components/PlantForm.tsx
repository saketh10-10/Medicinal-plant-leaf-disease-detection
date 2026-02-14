import { useState, useEffect } from 'react';

interface Plant {
  id?: number;
  name: string;
  species: string;
  careLevel: string;
  wateringFrequency: string;
  sunlight: string;
  description: string;
  lastWatered: string;
}

interface PlantFormProps {
  plant?: Plant | null;
  onSubmit: (plant: Omit<Plant, 'id'>) => void;
  onCancel: () => void;
}

const PlantForm = ({ plant, onSubmit, onCancel }: PlantFormProps) => {
  const [formData, setFormData] = useState<Omit<Plant, 'id'>>({
    name: '',
    species: '',
    careLevel: 'Medium',
    wateringFrequency: 'Weekly',
    sunlight: 'Medium indirect light',
    description: '',
    lastWatered: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    if (plant) {
      setFormData({
        name: plant.name,
        species: plant.species,
        careLevel: plant.careLevel,
        wateringFrequency: plant.wateringFrequency,
        sunlight: plant.sunlight,
        description: plant.description,
        lastWatered: plant.lastWatered
      });
    }
  }, [plant]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    if (!plant) {
      // Reset form for new plant
      setFormData({
        name: '',
        species: '',
        careLevel: 'Medium',
        wateringFrequency: 'Weekly',
        sunlight: 'Medium indirect light',
        description: '',
        lastWatered: new Date().toISOString().split('T')[0]
      });
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        {plant ? 'Edit Plant' : 'Add New Plant'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Plant Name *
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="e.g., Snake Plant"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Species
          </label>
          <input
            type="text"
            name="species"
            value={formData.species}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="e.g., Sansevieria trifasciata"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Care Level
            </label>
            <select
              name="careLevel"
              value={formData.careLevel}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Watering Frequency
            </label>
            <input
              type="text"
              name="wateringFrequency"
              value={formData.wateringFrequency}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="e.g., Every 2-3 weeks"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Sunlight Requirements
          </label>
          <input
            type="text"
            name="sunlight"
            value={formData.sunlight}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="e.g., Low to bright indirect light"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Add notes about this plant..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Last Watered
          </label>
          <input
            type="date"
            name="lastWatered"
            value={formData.lastWatered}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        <div className="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            {plant ? 'Update Plant' : 'Add Plant'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PlantForm;
