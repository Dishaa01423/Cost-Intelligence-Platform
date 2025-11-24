CSS_STYLES = """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: rgba(240, 242, 246, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: rgba(255, 243, 205, 0.15);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        color: inherit;
    }
    .insight-box h4, .insight-box p, .insight-box ul, .insight-box li {
        color: inherit !important;
    }
    .alert-box {
        background-color: rgba(248, 215, 218, 0.15);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        color: inherit;
    }
    .alert-box h4, .alert-box p, .alert-box strong, .alert-box ul, .alert-box li {
        color: inherit !important;
    }
    .success-box {
        background-color: rgba(212, 237, 218, 0.15);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: inherit;
    }
    .success-box h4, .success-box h3, .success-box p, .success-box strong, .success-box ul, .success-box li {
        color: inherit !important;
    }

    /* Dark mode specific overrides */
    @media (prefers-color-scheme: dark) {
        .insight-box {
            background-color: rgba(255, 193, 7, 0.1);
            border-left-color: #ffc107;
        }
        .alert-box {
            background-color: rgba(220, 53, 69, 0.1);
            border-left-color: #dc3545;
        }
        .success-box {
            background-color: rgba(40, 167, 69, 0.1);
            border-left-color: #28a745;
        }
    }
    </style>
"""