from shiny import App, ui, render
from flask import request

app_ui = ui.page_fluid(
    ui.h1("Client IP and Request Information"),
    
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
    @render.text
    def forwarded_for():
        x_forwarded_for = request.headers.get("X-Forwarded-For", "Not available")
        return f"X-Forwarded-For: {x_forwarded_for}"
    
    @render.text
    def remote_addr():
        remote_addr = request.remote_addr or "Not available"
        return f"Remote Address: {remote_addr}"
    
    @render.ui
    def formatted_headers():
        # Create a prettier display of headers with a table
        headers = []
        for name, value in request.headers.items():
            headers.append(ui.tags.tr(
                ui.tags.td(ui.strong(name)), 
                ui.tags.td(value)
            ))
        
        if not headers:
            return ui.p("No headers found")
        
        return ui.tags.table(
            ui.tags.thead(
                ui.tags.tr(
                    ui.tags.th("Header Name"),
                    ui.tags.th("Value")
                )
            ),
            ui.tags.tbody(*headers),
            class_="table table-striped table-bordered"
        )
    
    @render.ui
    def request_details():
        # Display other useful request information
        details = [
            ("Method", request.method),
            ("Path", request.path),
            ("User Agent", request.user_agent.string),
            ("Referrer", request.referrer or "None"),
            ("Is Secure", str(request.is_secure)),
            ("Host", request.host),
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
