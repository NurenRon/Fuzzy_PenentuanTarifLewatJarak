// Membaca data transaksi dengan aman dari element script JSON di index.html
const chartData = JSON.parse(document.getElementById('riwayat-data').textContent || '[]').reverse();

// --- 1. INISIALISASI GRAFIK TREN KECEPATAN VS HARGA ---
const ctx = document.getElementById('trendChart').getContext('2d');
if (chartData.length > 0) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.map(d => d.id),
            datasets: [{
                label: 'Tarif Akhir (Rp)',
                data: chartData.map(d => d.harga),
                borderColor: '#4edea3',
                backgroundColor: 'rgba(78, 222, 163, 0.2)',
                yAxisID: 'y',
                tension: 0.4,
                fill: true
            }, {
                label: 'Kecepatan (km/jam)',
                data: chartData.map(d => d.kecepatan),
                borderColor: '#ffb95f',
                backgroundColor: 'transparent',
                yAxisID: 'y1',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: { color: '#dce2f7' }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#bbcabf' },
                    grid: { color: 'rgba(60, 74, 66, 0.5)' }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: { color: '#4edea3' },
                    grid: { color: 'rgba(60, 74, 66, 0.5)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    ticks: { color: '#ffb95f' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
} else {
    document.getElementById('trendChart').parentElement.innerHTML = '<span class="text-on-surface-variant">Belum ada data untuk grafik</span>';
}

// --- 2. SET TANGGAL SAAT INI ---
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
document.getElementById('current-date').textContent = new Date().toLocaleDateString('id-ID', options);

// --- 3. LOGIKA GRAFIK FUNGSI KEANGGOTAAN FUZZY (MEMBERSHIP FUNCTIONS) ---
try {
    function trimf(x, abc) {
        const [a, b, c] = abc;
        if (x <= a || x >= c) return 0;
        if (x === b) return 1;
        if (x > a && x < b) return (x - a) / (b - a);
        if (x > b && x < c) return (c - x) / (c - b);
        return 0;
    }

    function trapmf(x, abcd) {
        const [a, b, c, d] = abcd;
        if (x <= a || x >= d) return 0;
        if (x >= b && x <= c) return 1;
        if (x > a && x < b) return (x - a) / (b - a);
        if (x > c && x < d) return (d - x) / (d - c);
        return 0;
    }

    const range = (start, stop, step) => Array.from({ length: Math.round((stop - start) / step) + 1}, (_, i) => parseFloat((start + (i * step)).toFixed(2)));

    const kecepatanDomain = range(0, 60, 1);
    const jarakDomain = range(0, 50, 1);
    const pengaliDomain = range(1.0, 3.0, 0.05);

    const fuzzyChartData = {
        kecepatan: {
            labels: kecepatanDomain,
            title: 'Kecepatan Kendaraan (km/jam)',
            datasets: [
                {
                    label: 'Macet (0 - 20 km/jam)',
                    data: kecepatanDomain.map(x => trimf(x, [0, 0, 20])),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Ramai Lancar (10 - 50 km/jam)',
                    data: kecepatanDomain.map(x => trimf(x, [10, 30, 50])),
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Lancar (40 - 60 km/jam)',
                    data: kecepatanDomain.map(x => trapmf(x, [40, 50, 60, 60])),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        jarak: {
            labels: jarakDomain,
            title: 'Jarak Pengiriman (km)',
            datasets: [
                {
                    label: 'Dekat (0 - 15 km)',
                    data: jarakDomain.map(x => trimf(x, [0, 0, 15])),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Sedang (10 - 40 km)',
                    data: jarakDomain.map(x => trimf(x, [10, 25, 40])),
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Jauh (30 - 50 km)',
                    data: jarakDomain.map(x => trapmf(x, [30, 40, 50, 50])),
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        pengali: {
            labels: pengaliDomain,
            title: 'Faktor Pengali Tarif (Surge Multiplier)',
            datasets: [
                {
                    label: 'Normal (1.0 - 1.5x)',
                    data: pengaliDomain.map(x => trimf(x, [1.0, 1.0, 1.5])),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Naik Sedang (1.3 - 2.3x)',
                    data: pengaliDomain.map(x => trimf(x, [1.3, 1.8, 2.3])),
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Surge Pricing (2.0 - 3.0x)',
                    data: pengaliDomain.map(x => trimf(x, [2.0, 3.0, 3.0])),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.1
                }
            ]
        }
    };

    const fuzzyCanvas = document.getElementById('fuzzyChart');
    if (fuzzyCanvas && typeof Chart !== 'undefined') {
        const fuzzyCtx = fuzzyCanvas.getContext('2d');
        const fuzzyChart = new Chart(fuzzyCtx, {
            type: 'line',
            data: {
                labels: fuzzyChartData.kecepatan.labels,
                datasets: fuzzyChartData.kecepatan.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#dce2f7', font: { family: 'Inter' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: µ = ${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Kecepatan Kendaraan (km/jam)',
                            color: '#bbcabf',
                            font: { family: 'Inter', size: 11 }
                        },
                        ticks: { color: '#bbcabf' },
                        grid: { color: 'rgba(60, 74, 66, 0.3)' }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Derajat Keanggotaan (µ)',
                            color: '#bbcabf',
                            font: { family: 'Inter', size: 11 }
                        },
                        min: 0,
                        max: 1.05,
                        ticks: { color: '#bbcabf', stepSize: 0.2 },
                        grid: { color: 'rgba(60, 74, 66, 0.3)' }
                    }
                }
            }
        });

        const tabs = {
            kecepatan: document.getElementById('tab-kecepatan'),
            jarak: document.getElementById('tab-jarak'),
            pengali: document.getElementById('tab-pengali')
        };

        function switchTab(activeTabKey) {
            Object.keys(tabs).forEach(key => {
                if (!tabs[key]) return;
                if (key === activeTabKey) {
                    tabs[key].classList.add('bg-primary', 'text-surface', 'font-bold');
                    tabs[key].classList.remove('text-on-surface-variant', 'font-medium');
                } else {
                    tabs[key].classList.remove('bg-primary', 'text-surface', 'font-bold');
                    tabs[key].classList.add('text-on-surface-variant', 'font-medium');
                }
            });

            fuzzyChart.data.labels = fuzzyChartData[activeTabKey].labels;
            fuzzyChart.data.datasets = fuzzyChartData[activeTabKey].datasets;
            fuzzyChart.options.scales.x.title.text = fuzzyChartData[activeTabKey].title;
            fuzzyChart.update();
        }

        if (tabs.kecepatan) tabs.kecepatan.addEventListener('click', () => switchTab('kecepatan'));
        if (tabs.jarak) tabs.jarak.addEventListener('click', () => switchTab('jarak'));
        if (tabs.pengali) tabs.pengali.addEventListener('click', () => switchTab('pengali'));
    } else {
        console.error("Canvas fuzzyChart or Chart.js constructor not found.");
    }
} catch (err) {
    console.error("Error drawing fuzzy curves:", err);
}

// --- 4. EVEN LISTENER UNTUK TOMBOL HITUNG TARIF ---
document.getElementById('btn-hitung').addEventListener('click', async () => {
    const koridor = document.getElementById('input-koridor').value;
    const jarak = document.getElementById('input-jarak').value;

    if(!jarak) return alert("Masukkan jarak pengiriman!");

    const btn = document.getElementById('btn-hitung');
    const originalText = btn.innerHTML;
    btn.innerHTML = "Menghitung...";
    btn.disabled = true;

    try {
        const response = await fetch('/api/hitung', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ koridor: koridor, jarak: jarak })
        });
        const result = await response.json();

        if(result.status === 'success') {
            document.getElementById('val-kecepatan').innerHTML = `${result.kecepatan} <span class="text-sm font-normal text-on-surface-variant">km/jam</span>`;
            document.getElementById('val-pengali').innerText = `${result.pengali}x`;
            
            const formatRp = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(result.tarif_akhir);
            const formatBaseRp = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(result.tarif_awal);
            
            document.getElementById('val-harga').innerText = formatRp;
            document.getElementById('receipt-base').innerText = formatBaseRp;
            document.getElementById('receipt-multiplier').innerText = `x ${result.pengali}`;
            document.getElementById('receipt-total').innerText = formatRp;

            setTimeout(() => location.reload(), 2000);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Terjadi kesalahan saat menghitung tarif.");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
});
