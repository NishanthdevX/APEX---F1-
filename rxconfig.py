import reflex as rx

config = rx.Config(
    app_name="apex_f1",
    frontend_port=3000,
    backend_port=8001,
    api_url="http://localhost:8001",
    deploy_url="http://localhost:3000",
    cors_allowed_origins=["*"],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)
