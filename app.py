from shiny import App, ui, render
import os

app_ui = ui.page_fluid(
    ui.card(
        ui.card_header("Client IP Information"),
        ui.output_text("forwarded_for"),
        ui.output_text("remote_addr"),
        ui.output_text("all_headers"),
        ui.output_text("env_vars")
    )
)

def server(input, output, session):
    @render.text
    def forwarded_for():
        # Try to get from environment variables, which is how Posit Connect provides it
        x_forwarded_for = os.environ.get("HTTP_X_FORWARDED_FOR", "Not available from env")
        return f"X-Forwarded-For from environment: {x_forwarded_for}"
    
    @render.text
    def remote_addr():
        # Remote address might be in an environment variable
        remote_addr = os.environ.get("REMOTE_ADDR", "Not available from env")
        return f"Remote Address from environment: {remote_addr}"
    
    @render.text
    def all_headers():
        # Display all headers that might contain IP information
        headers = [
            f"X-Real-IP: {os.environ.get('HTTP_X_REAL_IP', 'Not available')}",
            f"X-Client-IP: {os.environ.get('HTTP_X_CLIENT_IP', 'Not available')}",
            f"CF-Connecting-IP: {os.environ.get('HTTP_CF_CONNECTING_IP', 'Not available')}"
        ]
        return "\n".join(headers)
    
    @render.text
    def env_vars():
        # Display some relevant environment variables that might help debugging
        env_vars = []
        for key in sorted(os.environ.keys()):
            if "ADDR" in key or "IP" in key or "HOST" in key or "FORWARD" in key:
                env_vars.append(f"{key}: {os.environ[key]}")
        
        if not env_vars:
            return "No relevant environment variables found"
        return "\n".join(env_vars)

app = App(app_ui, server)
