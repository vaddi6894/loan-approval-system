// Global variables
let currentPredictionData = null;
let charts = {};

// API Base URL
const API_BASE = "http://127.0.0.1:5000/api";

// Initialize the application
document.addEventListener("DOMContentLoaded", function () {
  initializeNavigation();
  initializeEventListeners();
  loadAnalytics();
});

// Navigation functionality
function initializeNavigation() {
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");
  const navItems = document.querySelectorAll(".nav-item");
  const sections = document.querySelectorAll(".content-section");

  // Sidebar toggle for mobile
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });
  }

  // Navigation item clicks
  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const targetSection = item.getAttribute("data-section");

      // Update active nav item
      navItems.forEach((nav) => nav.classList.remove("active"));
      item.classList.add("active");

      // Show target section
      sections.forEach((section) => {
        section.classList.remove("active");
        if (section.id === targetSection) {
          section.classList.add("active");
        }
      });

      // Close sidebar on mobile
      if (window.innerWidth <= 768) {
        sidebar.classList.remove("active");
      }
    });
  });
}

// Initialize event listeners
function initializeEventListeners() {
  // Loan prediction form
  const loanForm = document.getElementById("loanForm");
  if (loanForm) {
    loanForm.addEventListener("submit", handlePrediction);
  }

  // What-if analysis
  const runWhatIfBtn = document.getElementById("runWhatIf");
  if (runWhatIfBtn) {
    runWhatIfBtn.addEventListener("click", runWhatIfAnalysis);
  }

  // Recommendations
  const getRecommendationsBtn = document.getElementById("getRecommendations");
  if (getRecommendationsBtn) {
    getRecommendationsBtn.addEventListener("click", getRecommendations);
  }

  // Target probability slider
  const targetProbabilitySlider = document.getElementById("targetProbability");
  const targetProbabilityValue = document.getElementById(
    "targetProbabilityValue"
  );
  if (targetProbabilitySlider && targetProbabilityValue) {
    targetProbabilitySlider.addEventListener("input", (e) => {
      targetProbabilityValue.textContent = `${(e.target.value * 100).toFixed(
        0
      )}%`;
    });
  }
}

// Handle loan prediction
async function handlePrediction(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const data = {};
  formData.forEach((value, key) => {
    data[key] = isNaN(value) ? value : Number(value);
  });

  // Store current data for other features
  currentPredictionData = data;

  // Show loading state
  const resultDiv = document.getElementById("predictionResult");
  resultDiv.innerHTML = '<div class="loading"></div> Processing prediction...';

  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      displayPredictionResult(result);
      // Update other sections with new data
      updateProbabilityBreakdown(result);
    } else {
      resultDiv.innerHTML = `<div class="error-message">Error: ${
        result.error || "Unknown error occurred"
      }</div>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="error-message">Error: Could not connect to server. Please make sure the backend is running.</div>`;
    console.error(error);
  }
}

// Display prediction result
function displayPredictionResult(result) {
  const resultDiv = document.getElementById("predictionResult");
  const statusColor = result.status === "Approved" ? "#28a745" : "#dc3545";
  const probabilityPercent = (result.probability * 100).toFixed(2);

  resultDiv.innerHTML = `
        <div style="margin-top: 20px; padding: 15px; border-radius: 5px; background-color: #f8f9fa; border-left: 4px solid ${statusColor};">
            <h3 style="color: ${statusColor}; margin: 0 0 10px 0;">Prediction: ${
    result.status
  }</h3>
            <p style="margin: 0; font-size: 16px;">Approval Probability: <strong>${probabilityPercent}%</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">Stored in database: ${
              result.stored_in_db ? "Yes" : "No"
            }</p>
        </div>
    `;
}

// Update probability breakdown
function updateProbabilityBreakdown(result) {
  if (!currentPredictionData) return;

  // Get feature importance
  fetch(`${API_BASE}/feature-importance`)
    .then((response) => response.json())
    .then((data) => {
      if (data.feature_importance) {
        createProbabilityChart(data.feature_importance, result.probability);
      }
    })
    .catch((error) =>
      console.error("Error loading feature importance:", error)
    );
}

// Create probability breakdown chart
function createProbabilityChart(featureImportance, probability) {
  const ctx = document.getElementById("probabilityChart");
  if (!ctx) return;

  // Destroy existing chart
  if (charts.probability) {
    charts.probability.destroy();
  }

  // Prepare data for chart
  const features = Object.keys(featureImportance);
  const importance = Object.values(featureImportance);

  // Calculate weighted contributions
  const contributions = importance.map((imp) => imp * probability);

  charts.probability = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: features.map((f) =>
        f.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
      ),
      datasets: [
        {
          data: contributions,
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
            "#FF6384",
            "#C9CBCF",
            "#4BC0C0",
            "#FF6384",
          ],
          borderWidth: 3,
          borderColor: "#fff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            padding: 20,
            usePointStyle: true,
            color: "#333",
            font: {
              size: 12,
              weight: "bold",
            },
          },
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.parsed;
              const percentage = ((value / probability) * 100).toFixed(1);
              return `${label}: ${percentage}% contribution`;
            },
          },
        },
      },
    },
  });

  // Update details
  const detailsDiv = document.getElementById("probabilityDetails");
  if (detailsDiv) {
    detailsDiv.innerHTML = `
            <div class="metric-item">
                <div class="metric-value">${(probability * 100).toFixed(
                  1
                )}%</div>
                <div class="metric-label">Overall Probability</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${features.length}</div>
                <div class="metric-label">Features Analyzed</div>
            </div>
        `;
  }
}

// Run what-if analysis
async function runWhatIfAnalysis() {
  if (!currentPredictionData) {
    alert("Please make a prediction first to use What-If Analysis");
    return;
  }

  const featureSelect = document.getElementById("whatifFeature");
  const selectedFeature = featureSelect.value;

  // Define ranges for different features
  const ranges = {
    income_annum: [1000000, 20000000],
    loan_amount: [1000000, 50000000],
    loan_term: [2, 60],
    cibil_score: [300, 900],
  };

  const [minVal, maxVal] = ranges[selectedFeature] || [0, 100];

  try {
    const response = await fetch(`${API_BASE}/what-if`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input_data: currentPredictionData,
        feature_name: selectedFeature,
        min_val: minVal,
        max_val: maxVal,
        steps: 20,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      createWhatIfChart(result);
    } else {
      alert(`Error: ${result.error}`);
    }
  } catch (error) {
    alert("Error running What-If Analysis");
    console.error(error);
  }
}

// Create what-if analysis chart
function createWhatIfChart(data) {
  const ctx = document.getElementById("whatifChart");
  if (!ctx) return;

  // Destroy existing chart
  if (charts.whatif) {
    charts.whatif.destroy();
  }

  const values = data.results.map((r) => r.value);
  const probabilities = data.results.map((r) => r.probability * 100);

  charts.whatif = new Chart(ctx, {
    type: "line",
    data: {
      labels: values,
      datasets: [
        {
          label: "Approval Probability (%)",
          data: probabilities,
          borderColor: "#667eea",
          backgroundColor: "rgba(102, 126, 234, 0.2)",
          borderWidth: 4,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: "#667eea",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: `How ${data.feature.replace(
            /_/g,
            " "
          )} affects approval probability`,
          color: "#333",
          font: {
            size: 16,
            weight: "bold",
          },
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          callbacks: {
            label: function (context) {
              return `Probability: ${context.parsed.y.toFixed(1)}%`;
            },
          },
        },
        legend: {
          labels: {
            color: "#333",
            font: {
              size: 12,
              weight: "bold",
            },
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: data.feature.replace(/_/g, " "),
            color: "#333",
            font: {
              size: 14,
              weight: "bold",
            },
          },
          grid: {
            color: "rgba(0, 0, 0, 0.1)",
          },
          ticks: {
            color: "#333",
          },
        },
        y: {
          title: {
            display: true,
            text: "Approval Probability (%)",
            color: "#333",
            font: {
              size: 14,
              weight: "bold",
            },
          },
          min: 0,
          max: 100,
          grid: {
            color: "rgba(0, 0, 0, 0.1)",
          },
          ticks: {
            color: "#333",
          },
        },
      },
    },
  });
}

// Get recommendations
async function getRecommendations() {
  if (!currentPredictionData) {
    alert("Please make a prediction first to get recommendations");
    return;
  }

  const targetProbability = parseFloat(
    document.getElementById("targetProbability").value
  );

  try {
    const response = await fetch(`${API_BASE}/recommendations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...currentPredictionData,
        target_probability: targetProbability,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      displayRecommendations(result.recommendations);
    } else {
      alert(`Error: ${result.error}`);
    }
  } catch (error) {
    alert("Error getting recommendations");
    console.error(error);
  }
}

// Display recommendations
function displayRecommendations(recommendations) {
  const listDiv = document.getElementById("recommendationsList");
  if (!listDiv) return;

  if (!recommendations || recommendations.length === 0) {
    listDiv.innerHTML = `
      <div class="recommendation-item">
        <h4>No specific recommendations available</h4>
        <p>Try adjusting your target probability or make a prediction first to get personalized recommendations.</p>
      </div>`;
    return;
  }

  listDiv.innerHTML = recommendations
    .map(
      (rec) => `
        <div class="recommendation-item ${rec.type || "general"}">
            <h4>${rec.message}</h4>
            ${
              rec.current && rec.suggested
                ? `
                <p><strong>Current:</strong> ${formatValue(
                  rec.current,
                  rec.type
                )}</p>
                <p><strong>Suggested:</strong> ${formatValue(
                  rec.suggested,
                  rec.type
                )}</p>
            `
                : ""
            }
            ${rec.impact ? `<p><strong>Impact:</strong> ${rec.impact}</p>` : ""}
        </div>
    `
    )
    .join("");
}

// Format values for display
function formatValue(value, type) {
  if (value === null || value === undefined) return "N/A";

  if (type === "income" || type === "loan_amount") {
    return `₹${Number(value).toLocaleString()}`;
  } else if (type === "cibil") {
    return `${Number(value)} points`;
  } else if (type === "loan_term") {
    return `${Number(value)} months`;
  }
  return String(value);
}

// Load analytics dashboard
async function loadAnalytics() {
  try {
    const response = await fetch(`${API_BASE}/analytics/summary`);
    const data = await response.json();

    if (response.ok) {
      displayModelMetrics(data.model_metrics);
      createFeatureImportanceChart(data.feature_importance);
    }
  } catch (error) {
    console.error("Error loading analytics:", error);
  }
}

// Display model metrics
function displayModelMetrics(metrics) {
  const metricsDiv = document.getElementById("modelMetrics");
  if (!metricsDiv || !metrics) return;

  metricsDiv.innerHTML = `
        <div class="metric-item">
            <div class="metric-value">${(metrics.train_accuracy * 100).toFixed(
              1
            )}%</div>
            <div class="metric-label">Training Accuracy</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">${(metrics.test_accuracy * 100).toFixed(
              1
            )}%</div>
            <div class="metric-label">Test Accuracy</div>
        </div>
    `;
}

// Create feature importance chart
function createFeatureImportanceChart(featureImportance) {
  const ctx = document.getElementById("featureImportanceChart");
  if (!ctx || !featureImportance) return;

  // Destroy existing chart
  if (charts.featureImportance) {
    charts.featureImportance.destroy();
  }

  const features = Object.keys(featureImportance);
  const importance = Object.values(featureImportance);

  // Sort by importance
  const sortedData = features
    .map((feature, index) => ({
      feature: feature
        .replace(/_/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase()),
      importance: importance[index],
    }))
    .sort((a, b) => b.importance - a.importance);

  charts.featureImportance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sortedData.map((d) => d.feature),
      datasets: [
        {
          label: "Feature Importance",
          data: sortedData.map((d) => d.importance),
          backgroundColor: "rgba(102, 126, 234, 0.8)",
          borderColor: "#667eea",
          borderWidth: 2,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          callbacks: {
            label: function (context) {
              return `Importance: ${(context.parsed.x * 100).toFixed(2)}%`;
            },
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Importance Score",
            color: "#333",
            font: {
              size: 14,
              weight: "bold",
            },
          },
          grid: {
            color: "rgba(0, 0, 0, 0.1)",
          },
          ticks: {
            color: "#333",
          },
        },
        y: {
          grid: {
            color: "rgba(0, 0, 0, 0.1)",
          },
          ticks: {
            color: "#333",
            font: {
              size: 12,
            },
          },
        },
      },
    },
  });
}

// Load prediction history
async function loadHistory() {
  try {
    const response = await fetch(`${API_BASE}/history`);
    const data = await response.json();

    if (response.ok) {
      displayHistory(data.predictions);
    }
  } catch (error) {
    console.error("Error loading history:", error);
  }
}

// Display prediction history
function displayHistory(predictions) {
  const historyDiv = document.getElementById("historyList");
  if (!historyDiv) return;

  if (!predictions || predictions.length === 0) {
    historyDiv.innerHTML = "<p>No prediction history available.</p>";
    return;
  }

  historyDiv.innerHTML = predictions
    .map(
      (pred) => `
        <div class="history-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>${pred.predicted_status}</strong> - ${(
        pred.predicted_probability * 100
      ).toFixed(1)}% probability
                </div>
                <small>${new Date(pred.created_at).toLocaleDateString()}</small>
            </div>
            <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                Income: ₹${pred.income_annum?.toLocaleString() || "N/A"} | 
                Loan: ₹${pred.loan_amount?.toLocaleString() || "N/A"} | 
                CIBIL: ${pred.cibil_score || "N/A"}
            </div>
        </div>
    `
    )
    .join("");
}

// Auto-load history when history section is accessed
document.addEventListener("click", function (e) {
  if (e.target.closest('[data-section="history"]')) {
    setTimeout(loadHistory, 100);
  }
});
