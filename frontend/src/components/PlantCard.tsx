import { useState } from 'react';

interface Plant {
  id: number;
  name: string;
  species: string;
  careLevel: string;
  wateringFrequency: string;
  sunlight: string;
  description: string;
  lastWatered: string;
}

interface PlantCardProps {
  plant: Plant;
  onWater: (id: number) => void;
  onEdit: (plant: Plant) => void;
  onDelete: (id: number) => void;
}

const PlantCard = ({ plant, onWater, onEdit, onDelete }: PlantCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getCareLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const isOverdue = () => {
    const lastWatered = new Date(plant.lastWatered);
    const now = new Date();
    const daysSinceWatered = Math.floor((now.getTime() - lastWatered.getTime()) / (1000 * 60 * 60 * 24));

    // Simple logic: if it's been more than 7 days, consider it overdue
    return daysSinceWatered > 7;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-800">{plant.name}</h3>
          <p className="text-gray-600 italic">{plant.species}</p>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCareLevelColor(plant.careLevel)}`}>
          {plant.careLevel}
        </span>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">Last watered:</span>
          <span className={`text-sm ${isOverdue() ? 'text-red-600 font-semibold' : 'text-gray-600'}`}>
            {plant.lastWatered}
            {isOverdue() && ' ⚠️'}
          </span>
        </div>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Watering:</span> {plant.wateringFrequency}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Light:</span> {plant.sunlight}
        </p>
      </div>

      {isExpanded && (
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <p className="text-sm text-gray-700">{plant.description}</p>
        </div>
      )}

      <div className="flex justify-between items-center">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          {isExpanded ? 'Show less' : 'Show more'}
        </button>

        <div className="flex space-x-2">
          <button
            onClick={() => onWater(plant.id)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm"
          >
            💧 Water
          </button>
          <button
            onClick={() => onEdit(plant)}
            className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm"
          >
            ✏️ Edit
          </button>
          <button
            onClick={() => onDelete(plant.id)}
            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
          >
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default PlantCard;
