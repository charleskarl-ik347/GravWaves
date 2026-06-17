async function runAnalysis() {
    const lowCutInput = document.getElementById("lowCut");
    const highCutInput = document.getElementById("highCut");

    const lowValue = document.getElementById("lowValue");
    const highValue = document.getElementById("highValue");

    const lowCut = Number(lowCutInput.value);
    const highCut = Number(highCutInput.value);

    lowValue.textContent = lowCut;
    highValue.textContent = highCut;

    if (lowCut >= highCut) {
        alert("Low cutoff must be smaller than high cutoff.");
        return;
    }

    try {
        const response = await fetch(
            `/api/analyze?low=${lowCut}&high=${highCut}`
        );

        if (!response.ok) {
            throw new Error("Python backend did not respond correctly.");
        }

        const data = await response.json();

        plotRaw(data.time, data.raw_signal);
        plotSpectrum(data.frequencies, data.magnitude, lowCut, highCut);
        plotFiltered(data.time, data.raw_signal, data.reconstructed_signal);

    } catch (error) {
        console.error(error);
        alert("Could not connect to the Python backend. Make sure python app.py is running.");
    }
}

function getPlotLayout(title, xTitle, yTitle) {
    return {
        title: {
            text: title,
            font: {
                color: "#e5e7eb",
                size: 17
            },
            x: 0.03
        },
        autosize: true,
        height: 430,
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: {
            color: "#e5e7eb",
            family: "Inter, system-ui, sans-serif"
        },
        xaxis: {
            title: {
                text: xTitle,
                standoff: 12
            },
            gridcolor: "#1f2937",
            zerolinecolor: "#263244",
            tickcolor: "#263244",
            linecolor: "#263244",
            automargin: true
        },
        yaxis: {
            title: {
                text: yTitle,
                standoff: 12
            },
            gridcolor: "#1f2937",
            zerolinecolor: "#263244",
            tickcolor: "#263244",
            linecolor: "#263244",
            automargin: true
        },
        margin: {
            l: 72,
            r: 28,
            t: 68,
            b: 64
        },
        legend: {
            orientation: "h",
            x: 0,
            y: -0.22
        }
    };
}

function getPlotConfig() {
    return {
        responsive: true,
        displaylogo: false
    };
}

function plotRaw(time, rawSignal) {
    const trace = {
        x: time,
        y: rawSignal,
        mode: "lines",
        name: "Raw Signal",
        line: {
            width: 1.5
        }
    };

    const layout = getPlotLayout(
        "Raw Noisy Time-Domain Signal",
        "Time (seconds)",
        "Amplitude"
    );

    Plotly.react("rawPlot", [trace], layout, getPlotConfig());
}

function plotSpectrum(frequencies, magnitude, lowCut, highCut) {
    const maxMagnitude = Math.max(...magnitude);

    const spectrumTrace = {
        x: frequencies,
        y: magnitude,
        mode: "lines",
        name: "Frequency Spectrum",
        line: {
            width: 1.5
        }
    };

    const lowLine = {
        x: [lowCut, lowCut],
        y: [0, maxMagnitude],
        mode: "lines",
        name: "Low Cutoff",
        line: {
            width: 1,
            dash: "dash"
        }
    };

    const highLine = {
        x: [highCut, highCut],
        y: [0, maxMagnitude],
        mode: "lines",
        name: "High Cutoff",
        line: {
            width: 1,
            dash: "dash"
        }
    };

    const layout = getPlotLayout(
        "Frequency Spectrum from Fourier Analysis",
        "Frequency (Hz)",
        "Magnitude"
    );

    layout.xaxis.range = [0, 300];

    Plotly.react(
        "spectrumPlot",
        [spectrumTrace, lowLine, highLine],
        layout,
        getPlotConfig()
    );
}

function plotFiltered(time, rawSignal, reconstructed) {
    const rawTrace = {
        x: time,
        y: rawSignal,
        mode: "lines",
        name: "Raw Signal",
        opacity: 0.45,
        line: {
            width: 1
        }
    };

    const filteredTrace = {
        x: time,
        y: reconstructed,
        mode: "lines",
        name: "Filtered Reconstruction",
        line: {
            width: 2
        }
    };

    const layout = getPlotLayout(
        "Raw Signal vs Filtered Reconstruction",
        "Time (seconds)",
        "Amplitude"
    );

    Plotly.react(
        "filteredPlot",
        [rawTrace, filteredTrace],
        layout,
        getPlotConfig()
    );
}

function setupControls() {
    const lowCut = document.getElementById("lowCut");
    const highCut = document.getElementById("highCut");
    const lowValue = document.getElementById("lowValue");
    const highValue = document.getElementById("highValue");
    const runButton = document.getElementById("run-analysis");

    lowCut.addEventListener("input", function () {
        lowValue.textContent = this.value;
    });

    highCut.addEventListener("input", function () {
        highValue.textContent = this.value;
    });

    runButton.addEventListener("click", runAnalysis);
}

setupControls();
runAnalysis();
