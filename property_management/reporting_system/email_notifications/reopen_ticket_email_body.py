def email_body(artifacts:dict):


    body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            height: 100vh;
        }}

        .header {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }}

        .logo {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .helix-text {{
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
        }}

        .property-text {{
            font-size: 24px;
            color: #555555;
        }}

        .management-text {{
            font-size: 18px;
            color: #777777;
        }}

        .welcome-text {{
            font-size: 24px;
            color: #333333;
            margin-top: 20px;
        }}

        .helix-svg {{
            width: 100px;
            height: 100px;
            margin-top: 10px;
            fill: #3498db; /* Adjust the fill color as needed */
        }}

        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            color: #333333;
        }}

        p {{
            color: #555555;
        }}

        .cta-button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: rgb(4, 58, 145);
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 5px;
        }}

        .cta-button:hover {{
            background-color: rgb(4, 58, 145);
        }}

    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
        <div class="helix-text">PEACH STREET</div>
        </div>

    </div>
    <div class="container">
        <h1 style="color: rgb(4, 58, 145)">Ticket #{artifacts['ticket_num']} was re-opened.</h1>
        <p>Dear user,</p>
        <p>{artifacts['username']} has set the following issue to {artifacts['status']}.</p>
        </br>
        <p>Issue: {artifacts['issue']}</p>
        <p>Updated on: {artifacts['date']}</p>

    
        
        <a class="cta-button" href="https://peachstreet.io/home">View Ticket</a>
    </div>
</body>
</html>
    """
    return body