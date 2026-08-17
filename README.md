<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>My DevOps Project</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            text-align: center;
            padding-top: 100px;
        }

        .container {
            background: white;
            width: 500px;
            max-width: 90%;
            margin: auto;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        h1 {
            color: #0078d4;
        }

        p {
            color: #555;
        }

        button {
            padding: 12px 25px;
            background: #0078d4;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #005a9e;
        }
    </style>
</head>

<body>

    <div class="container">

        <h1>Hello DevOps 🚀</h1>

        <p>
            This is my first HTML project pushed to DevOps.
        </p>

        <button onclick="showMessage()">
            Click Me
        </button>

        <p id="message"></p>

    </div>

    <script>
        function showMessage() {
            document.getElementById("message").textContent =
                "Successfully running my DevOps project!";
        }
    </script>

</body>
</html>
