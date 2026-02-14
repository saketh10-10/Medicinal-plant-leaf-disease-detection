import { useEffect, useState } from 'react';
import { CheckCircle, AlertTriangle, Leaf, Microscope, Loader2 } from 'lucide-react';

interface DiseaseInfo {
  name: string;
  severity: string;
  symptoms: string[];
  remedies: string[];
}

interface AnalysisResultsProps {
  isAnalyzing: boolean;
  analysisData?: {
    scientific_name: string;
    common_name: string;
    confidence: number;
    medicinal_properties: string[];
    plant_health_status: string;
    detected_diseases?: DiseaseInfo[] | null;
    care_recommendations: string[];
  } | null;
}

const AnalysisResults = ({ isAnalyzing, analysisData }: AnalysisResultsProps) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (isAnalyzing) {
      setProgress(0);
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + 10;
        });
      }, 250);
      return () => clearInterval(interval);
    }
  }, [isAnalyzing]);

  if (isAnalyzing) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="glass-card rounded-3xl p-8 border border-primary/20">
          <div className="text-center space-y-8">
            <div className="flex items-center justify-center">
              <div className="relative">
                <div className="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center">
                  <Loader2 className="w-12 h-12 text-primary animate-spin" />
                </div>
                <div className="absolute inset-0 rounded-full border-4 border-primary/20 animate-ping"></div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-foreground">Analyzing Your Plant</h3>
              <p className="text-muted-foreground">
                Our AI is examining the leaf for diseases and identifying medicinal properties...
              </p>
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Analysis Progress</span>
                <span className="font-semibold text-primary">{progress}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-accent h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
              {[
                { icon: Microscope, label: 'Disease Detection', status: progress > 30 ? 'completed' : 'pending' },
                { icon: Leaf, label: 'Species Identification', status: progress > 60 ? 'completed' : 'pending' },
                { icon: CheckCircle, label: 'Medicinal Properties', status: progress > 90 ? 'completed' : 'pending' }
              ].map((step, index) => (
                <div key={index} className="flex items-center gap-3 p-3 rounded-xl bg-muted/50">
                  <div className={`p-2 rounded-lg ${step.status === 'completed' ? 'bg-primary/20 text-primary' : 'bg-muted text-muted-foreground'}`}>
                    <step.icon className="w-4 h-4" />
                  </div>
                  <span className="text-sm font-medium">{step.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="glass-card rounded-3xl p-8 border border-primary/20">
        <div className="text-center space-y-8">
          <div className="flex items-center justify-center">
            <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-3xl font-bold text-foreground">Analysis Complete!</h3>
            <p className="text-muted-foreground text-lg">
              We've successfully analyzed your plant sample
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-2xl bg-green-50 border border-green-200">
              <div className="flex items-center gap-3 mb-3">
                <Leaf className="w-6 h-6 text-green-600" />
                <h4 className="text-lg font-semibold text-green-800">Plant Identified</h4>
              </div>
              <p className="text-green-700 font-medium">{analysisData?.common_name || 'Unknown'}</p>
              <p className="text-green-600 text-sm mt-1 italic">{analysisData?.scientific_name || ''}</p>
              <p className="text-green-600 text-sm mt-2">
                {(analysisData?.confidence || 0).toFixed(2)}% confidence
              </p>
            </div>

            <div className={`p-6 rounded-2xl border ${
              analysisData?.plant_health_status === 'Healthy'
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center gap-3 mb-3">
                <CheckCircle className={`w-6 h-6 ${
                  analysisData?.plant_health_status === 'Healthy' ? 'text-green-600' : 'text-red-600'
                }`} />
                <h4 className={`text-lg font-semibold ${
                  analysisData?.plant_health_status === 'Healthy' ? 'text-green-800' : 'text-red-800'
                }`}>
                  Health Status
                </h4>
              </div>
              <p className={`font-medium ${
                analysisData?.plant_health_status === 'Healthy' ? 'text-green-700' : 'text-red-700'
              }`}>
                {analysisData?.plant_health_status || 'Unknown'}
              </p>
              <p className={`text-sm mt-1 ${
                analysisData?.plant_health_status === 'Healthy' ? 'text-green-600' : 'text-red-600'
              }`}>
                Plant condition assessment
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-purple-50 border border-purple-200 md:col-span-2">
              <div className="flex items-center gap-3 mb-3">
                <Microscope className="w-6 h-6 text-purple-600" />
                <h4 className="text-lg font-semibold text-purple-800">Medicinal Properties</h4>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                {analysisData?.medicinal_properties?.map((property, index) => (
                  <div key={index} className="text-purple-700">• {property}</div>
                )) || (
                  <div className="text-purple-600 col-span-full">No medicinal properties available</div>
                )}
              </div>
            </div>

            {analysisData?.detected_diseases && analysisData.detected_diseases.length > 0 && (
              <div className="p-6 rounded-2xl bg-red-50 border border-red-200 md:col-span-2">
                <div className="flex items-center gap-3 mb-4">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                  <h4 className="text-lg font-semibold text-red-800">Detected Diseases</h4>
                </div>
                <div className="space-y-4">
                  {analysisData.detected_diseases.map((disease, index) => (
                    <div key={index} className="border border-red-200 rounded-lg p-4 bg-white/50">
                      <div className="flex items-center justify-between mb-2">
                        <h5 className="font-semibold text-red-800">{disease.name}</h5>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          disease.severity === 'High' ? 'bg-red-100 text-red-800' :
                          disease.severity === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {disease.severity} Severity
                        </span>
                      </div>

                      <div className="space-y-2">
                        <div>
                          <p className="text-sm font-medium text-red-700 mb-1">Symptoms:</p>
                          <ul className="text-sm text-red-600 ml-4 list-disc">
                            {disease.symptoms.map((symptom, symptomIndex) => (
                              <li key={symptomIndex}>{symptom}</li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <p className="text-sm font-medium text-red-700 mb-1">Remedies:</p>
                          <ul className="text-sm text-red-600 ml-4 list-disc">
                            {disease.remedies.map((remedy, remedyIndex) => (
                              <li key={remedyIndex}>{remedy}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="mt-8 p-4 rounded-xl bg-yellow-50 border border-yellow-200">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div className="text-left">
                <p className="text-yellow-800 font-medium">Care Recommendations</p>
                <div className="text-yellow-700 text-sm mt-1">
                  {analysisData?.care_recommendations?.map((recommendation, index) => (
                    <div key={index} className="mb-1">• {recommendation}</div>
                  )) || (
                    <div>No care recommendations available</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
