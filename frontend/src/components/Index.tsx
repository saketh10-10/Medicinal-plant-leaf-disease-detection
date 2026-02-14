import { useState } from "react";

import { ImageUpload } from "./ImageUpload";

import AnalysisResults from "./AnalysisResults";

import FloatingParticles from "./FloatingParticles";

import { Button } from "./ui/button";

import { Leaf, Sparkles, ChevronRight } from "lucide-react";

import heroImage from "../assets/hero_background.png";

import { api } from "../services/api";



const Index = () => {

  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  const [analysisData, setAnalysisData] = useState<any>(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [showResults, setShowResults] = useState(false);



  const analyzeImage = async (file: File) => {
    setIsAnalyzing(true);
    setShowResults(true);

    try {
      // Call the backend analyze endpoint
      const response = await api.analyze(file);

      // Store the analysis result
      setAnalysisData(response);

      setIsAnalyzing(false);
    } catch (error) {
      alert(`❌ Error: ${error instanceof Error ? error.message : 'Failed to analyze image'}`);
      setIsAnalyzing(false);
      setShowResults(false);
      setAnalysisData(null);
    }
  };



  const handleImageSelect = async (file: File | null) => {
    setSelectedImage(file);
    setAnalysisData(null);

    if (file) {
      // Automatically analyze the image when selected
      await analyzeImage(file);
    } else {
      setShowResults(false);
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {

    setSelectedImage(null);

    setAnalysisData(null);

    setShowResults(false);

    setIsAnalyzing(false);

  };



  const handleNewAnalysis = () => {

    setSelectedImage(null);

    setAnalysisData(null);

    setShowResults(false);

    setIsAnalyzing(false);

  };



  return (

    <div className="min-h-screen relative">

      <FloatingParticles />



      {/* Hero Section */}
      <section className="relative overflow-hidden min-h-screen flex items-center justify-center">
        <div className="absolute inset-0 opacity-20">
          <img
            src={heroImage}
            alt="Medicinal plant leaves"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background via-background/60 to-background" />
        </div>

        <div className="relative container mx-auto px-4 py-20 z-10">
          <div className="max-w-5xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full glass-card border border-primary/20 shadow-[0_0_30px_rgba(74,222,128,0.1)] animate-slide-up">
              <Sparkles className="w-4 h-4 text-primary animate-pulse" />
              <span className="text-sm font-semibold text-primary tracking-wider">AI-POWERED BOTANICAL ANALYSIS</span>
            </div>

            <h1 className="text-7xl md:text-9xl font-heading font-bold text-foreground leading-tight tracking-tight animate-slide-up drop-shadow-2xl" style={{ animationDelay: '0.1s' }}>
              Medicinal Plant
              <span className="block mt-2 bg-gradient-to-r from-green-400 via-yellow-400 to-green-400 bg-clip-text text-transparent animate-pulse drop-shadow-sm">
                Disease Detection
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-muted-foreground/80 max-w-3xl mx-auto leading-relaxed animate-slide-up font-light" style={{ animationDelay: '0.2s' }}>
              Harness the power of artificial intelligence to identify medicinal plants,
              discover their healing properties, and detect diseases with unprecedented accuracy.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-6 pt-8 animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <div className="flex items-center gap-3 px-6 py-3 rounded-2xl glass-card border border-primary/10 hover:bg-white/5 transition-colors">
                <div className="w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_10px_rgba(74,222,128,0.5)]" />
                <span className="text-base text-muted-foreground">Instant Analysis</span>
              </div>
              <div className="flex items-center gap-3 px-6 py-3 rounded-2xl glass-card border border-primary/10 hover:bg-white/5 transition-colors">
                <div className="w-2.5 h-2.5 rounded-full bg-accent shadow-[0_0_10px_rgba(251,191,36,0.5)]" />
                <span className="text-base text-muted-foreground">94% Accuracy</span>
              </div>
              <div className="flex items-center gap-3 px-6 py-3 rounded-2xl glass-card border border-primary/10 hover:bg-white/5 transition-colors">
                <div className="w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_10px_rgba(74,222,128,0.5)]" />
                <span className="text-base text-muted-foreground">1000+ Species</span>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-1/4 left-10 w-64 h-64 rounded-full bg-primary/5 blur-[100px] animate-pulse" />
        <div className="absolute bottom-1/4 right-10 w-80 h-80 rounded-full bg-accent/5 blur-[100px] animate-pulse" style={{ animationDelay: '1s' }} />
      </section>



      {/* Main Content */}

      <section className="relative container mx-auto px-4 py-16 md:py-24">

        <div className="space-y-12">

          {!showResults && (

            <div className="space-y-8 animate-slide-up">

              <ImageUpload

                onImageSelect={handleImageSelect}

                selectedImage={selectedImage}

                onClear={handleClear}

              />




            </div>

          )}



          {showResults && (

            <div className="space-y-8">

              <AnalysisResults isAnalyzing={isAnalyzing} analysisData={analysisData} />



              {!isAnalyzing && (

                <div className="flex justify-center animate-slide-up">

                  <Button

                    size="lg"

                    variant="secondary"

                    onClick={handleNewAnalysis}

                    className="gap-3 text-lg px-10 group"

                  >

                    <Leaf className="w-6 h-6 group-hover:rotate-12 transition-transform" />

                    Analyze Another Leaf

                    <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />

                  </Button>

                </div>

              )}

            </div>

          )}

        </div>

      </section>



      {/* Footer */}

      <footer className="relative container mx-auto px-4 py-12 mt-24 border-t border-primary/20">

        <div className="max-w-4xl mx-auto">

          <div className="glass-card rounded-2xl p-8 border border-primary/20">

            <div className="flex flex-col md:flex-row items-center justify-between gap-6">

              <div className="flex items-center gap-3">

                <div className="p-3 rounded-xl gradient-primary shadow-glow">

                  <Leaf className="w-6 h-6 text-primary-foreground" />

                </div>

                <div>

                  <p className="font-heading text-lg text-foreground">MediLeaf AI</p>

                  <p className="text-sm text-muted-foreground">Advanced botanical analysis system</p>

                </div>

              </div>

              <div className="flex items-center gap-2 text-sm text-muted-foreground">

                <Sparkles className="w-4 h-4 text-primary" />

                <span>Powered by cutting-edge AI • Frontend demo</span>

              </div>

            </div>

          </div>

        </div>

      </footer>

    </div>

  );

};



export default Index;
