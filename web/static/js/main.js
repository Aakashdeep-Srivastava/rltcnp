// Main JavaScript file for RTL Combinational Depth Predictor

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Add smooth scrolling for all links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Add tooltip initialization if Bootstrap is loaded
  if (typeof bootstrap !== "undefined") {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
});

// Format numbers with 2 decimal places
function formatNumber(num) {
  return parseFloat(num).toFixed(2);
}

// Show an error message
function showError(message) {
  const errorDiv = document.createElement("div");
  errorDiv.className = "alert alert-danger alert-dismissible fade show";
  errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  // Insert at the top of the container
  const container = document.querySelector(".container");
  container.insertBefore(errorDiv, container.firstChild);

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    const alert = new bootstrap.Alert(errorDiv);
    alert.close();
  }, 5000);
}

// Show a success message
function showSuccess(message) {
  const successDiv = document.createElement("div");
  successDiv.className = "alert alert-success alert-dismissible fade show";
  successDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  // Insert at the top of the container
  const container = document.querySelector(".container");
  container.insertBefore(successDiv, container.firstChild);

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    const alert = new bootstrap.Alert(successDiv);
    alert.close();
  }, 5000);
}

// Create a simple bar chart using HTML/CSS (fallback if Chart.js is not available)
function createSimpleBarChart(containerId, labels, data, maxValue) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  // Create chart container
  const chartDiv = document.createElement("div");
  chartDiv.className = "simple-chart";

  // Add bars
  for (let i = 0; i < labels.length; i++) {
    const barContainer = document.createElement("div");
    barContainer.className = "bar-container";

    const labelDiv = document.createElement("div");
    labelDiv.className = "bar-label";
    labelDiv.textContent = labels[i];

    const barWrapperDiv = document.createElement("div");
    barWrapperDiv.className = "bar-wrapper";

    const barDiv = document.createElement("div");
    barDiv.className = "bar";
    barDiv.style.width = `${(data[i] / maxValue) * 100}%`;

    const valueDiv = document.createElement("div");
    valueDiv.className = "bar-value";
    valueDiv.textContent = formatNumber(data[i]);

    barWrapperDiv.appendChild(barDiv);
    barWrapperDiv.appendChild(valueDiv);

    barContainer.appendChild(labelDiv);
    barContainer.appendChild(barWrapperDiv);

    chartDiv.appendChild(barContainer);
  }

  container.appendChild(chartDiv);
}

// Add CSS for the simple chart
const style = document.createElement("style");
style.textContent = `
    .simple-chart {
        margin: 20px 0;
    }
    .bar-container {
        display: flex;
        margin-bottom: 10px;
        align-items: center;
    }
    .bar-label {
        width: 150px;
        text-align: right;
        padding-right: 10px;
        font-size: 0.8rem;
    }
    .bar-wrapper {
        flex-grow: 1;
        display: flex;
        align-items: center;
        background-color: #f1f5f9;
        border-radius: 4px;
        overflow: hidden;
    }
    .bar {
        height: 20px;
        background-color: #0d6efd;
        border-radius: 4px;
    }
    .bar-value {
        margin-left: 10px;
        font-size: 0.8rem;
        color: #666;
    }
`;
document.head.appendChild(style);

// Handle sample file selection
$(".sample-file").on("click", function (e) {
  e.preventDefault();
  const filename = $(this).data("filename");

  // Show a message that the sample file is being processed
  showSuccess(`Processing sample file: ${filename}`);

  // Simulate loading signals for the sample file
  setTimeout(function () {
    currentFilename = filename;

    // Populate signal dropdown with sample signals
    const signalSelect = $("#signal-select");
    signalSelect.empty();
    signalSelect.append(
      '<option value="" selected disabled>Select a signal</option>'
    );

    // Add sample signals based on the file type
    if (filename === "counter.v") {
      signalSelect.append('<option value="count">count</option>');
      signalSelect.append('<option value="max_reached">max_reached</option>');
      signalSelect.append('<option value="overflow">overflow</option>');
    } else if (filename === "alu.v") {
      signalSelect.append('<option value="result">result</option>');
      signalSelect.append('<option value="zero_flag">zero_flag</option>');
      signalSelect.append(
        '<option value="overflow_flag">overflow_flag</option>'
      );
    } else if (filename === "fifo_controller.v") {
      signalSelect.append('<option value="data_out">data_out</option>');
      signalSelect.append('<option value="full">full</option>');
      signalSelect.append('<option value="empty">empty</option>');
      signalSelect.append(
        '<option value="debug_trigger">debug_trigger</option>'
      );
    } else if (filename === "fpu.v") {
      signalSelect.append('<option value="result">result</option>');
      signalSelect.append(
        '<option value="transcendental_result">transcendental_result</option>'
      );
      signalSelect.append(
        '<option value="exception_flag">exception_flag</option>'
      );
    } else if (filename === "dsp.v") {
      signalSelect.append(
        '<option value="filter_output">filter_output</option>'
      );
      signalSelect.append(
        '<option value="adaptive_filter_output">adaptive_filter_output</option>'
      );
      signalSelect.append('<option value="fft_result">fft_result</option>');
    }

    // Show signal selection card
    $("#signal-selection-card").removeClass("d-none");

    // Scroll to the signal selection card
    $("html, body").animate(
      {
        scrollTop: $("#signal-selection-card").offset().top - 20,
      },
      500
    );
  }, 500);
});
