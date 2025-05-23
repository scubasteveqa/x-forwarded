from shiny import App, ui, render, reactive
from flask import request

app_ui = ui.page_fluid(
    ui.h1("Client IP and Request Information"),
    
    ui.input_action_button("refresh", "Refresh Information", class_="btn-primary mb-3"),
    
    ui.card(
        ui.card_header("IP Address Information"),
        ui.output_text("forwarded_for"),
        ui.output_text("remote_addr"),
    ),
    
    ui.card(
        ui.card_header("All Request Headers"),
        ui.output_ui("formatted_headers"),
    ),
    
    ui.card(
        ui.card_header("Request Details"),
        ui.output_ui("request_details"),
    )
)

def server(input, output, session):
    # Use reactive.value to store request info
    req_info = reactive.value({})
    
    # Function to update request info (not decorated yet)
    def _update_request_info():
        # Store all the request information we need
        headers = {name: value for name, value in request.headers.items()}
        
        req_info.set({
            "x_forwarded_for": request.headers.get("X-Forwarded-For", "Not available"),
            "remote_addr": request.remote_addr or "Not available",
            "headers": headers,
            "method": request.method,
            "path": request.path,
            "user_agent": request.user_agent.string if request.user_agent else "Not available",
            "referrer": request.referrer or "None",
            "is_secure": str(request.is_secure),
            "host": request.host,
        })
    
    # First effect: trigger on refresh button
    @reactive.effect
    @reactive.event(input.refresh)
    def _():
        _update_request_info()
    
    # Second effect: trigger on session init
    @reactive.effect
    def _():
        _update_request_info()
    
    @render.text
    def forwarded_for():
        info = req_info()
        return f"X-Forwarded-For: {info.get('x_forwarded_for', 'No data yet')}"
    
    @render.text
    def remote_addr():
        info = req_info()
        return f"Remote Address: {info.get('remote_addr', 'No data yet')}"
    
    @render.ui
    def formatted_headers():
        info = req_info()
        headers = info.get("headers", {})
        
        if not headers:
            return ui.p("No headers found or data not loaded yet. Try clicking the Refresh button.")
        
        header_rows = []
        for name, value in headers.items():
            header_rows.append(ui.tags.tr(
                ui.tags.td(ui.strong(name)), 
                ui.tags.td(value)
            ))
        
        return ui.tags.table(
            ui.tags.thead(
                ui.tags.tr(
                    ui.tags.th("Header Name"),
                    ui.tags.th("Value")
                )
            ),
            ui.tags.tbody(*header_rows),
            class_="table table-striped table-bordered"
        )
    
    @render.ui
    def request_details():
        info = req_info()
        
        if not info:
            return ui.p("No request data loaded yet. Try clicking the Refresh button.")
        
        details = [
            ("Method", info.get("method", "")),
            ("Path", info.get("path", "")),
            ("User Agent", info.get("user_agent", "")),
            ("Referrer", info.get("referrer", "")),
            ("Is Secure", info.get("is_secure", "")),
            ("Host", info.get("host", "")),
        ]
        
        rows = []
        for name, value in details:
            rows.append(ui.tags.tr(
                ui.tags.td(ui.strong(name)),
                ui.tags.td(value)
            ))
        
        return ui.tags.table(
            ui.tags.tbody(*rows),
            class_="table table-striped table-bordered"
        )

app = App(app_ui, server)
