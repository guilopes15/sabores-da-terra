## Sabores da Terra - [1.0.0](https://github.com/guilopes15/sabores-da-terra/releases/1.0.0)

### Features

- Modeling the database tables with SQLAlchemy according to the flow diagram. ([#2](https://github.com/guilopes15/sabores-da-terra/issues/2))
- Adding routers for CRUD operations for Users, Products, Orders, and OrderItems. ([#3](https://github.com/guilopes15/sabores-da-terra/issues/3))
- Adding a user authentication system using the JWT token strategy. ([#4](https://github.com/guilopes15/sabores-da-terra/issues/4))
- Creating integration with the Stripe payment system. ([#5](https://github.com/guilopes15/sabores-da-terra/issues/5))
- Creating checkout and webhook routes. ([#5](https://github.com/guilopes15/sabores-da-terra/issues/5))
- Adding a notification system that sends an email when an order is paid and when a database error occurs. ([#6](https://github.com/guilopes15/sabores-da-terra/issues/6))
- Creating the possibility for an admin to manually register a sale in the system. ([#8](https://github.com/guilopes15/sabores-da-terra/issues/8))
- Creating a Telegram bot that interacts with the customer by typing a command, including a viewer of available products and redirect links to social media and the app's webpage. ([#9](https://github.com/guilopes15/sabores-da-terra/issues/9))
- Starting the front end in server-side rendering with Jinja templates, including registration and login screens, home page, individual pages for each product, shopping cart, and user profile page. ([#10](https://github.com/guilopes15/sabores-da-terra/issues/10))

- Added an admin panel that allows him to manage all products. ([#10](https://github.com/guilopes15/sabores-da-terra/issues/10))
- Implementing SuperUser (admin) permissions. ([#16](https://github.com/guilopes15/sabores-da-terra/issues/16))
- Implementing a refresh token for improved user navigation. ([#18](https://github.com/guilopes15/sabores-da-terra/issues/18))
- Adding updated_at fields to orders. ([#18](https://github.com/guilopes15/sabores-da-terra/issues/18))
- Adding the image field to the product model. ([#30](https://github.com/guilopes15/sabores-da-terra/issues/30))
- Improving the user experience by adding the option to press the enter key when typing the product name in the search field and creating a button to remove an item from the order. ([#33](https://github.com/guilopes15/sabores-da-terra/issues/33))
- Adding new features to the admin panel to view user and order data. ([#37](https://github.com/guilopes15/sabores-da-terra/issues/37))

### Bugfixes

- Correcting a bug that prevented products from being removed from a pending order when a product was deleted from the system. ([#22](https://github.com/guilopes15/sabores-da-terra/issues/22))
- Correcting a conceptual error between controller and service. ([#49](https://github.com/guilopes15/sabores-da-terra/issues/49))
- Fixing the error that freezes the execution flow when sending an email on the webhook route. ([#51](https://github.com/guilopes15/sabores-da-terra/issues/51))

### Improved Documentation

- Creating flowcharts according to business rules. ([#1](https://github.com/guilopes15/sabores-da-terra/issues/1))
- Creating the final documentation for the system. ([#41](https://github.com/guilopes15/sabores-da-terra/issues/41))

### Misc

- General refactoring of the project for better code architecture and organization. ([#20](https://github.com/guilopes15/sabores-da-terra/issues/20))
- Implementing lint and tests pipeline with GitHub workflows. ([#28](https://github.com/guilopes15/sabores-da-terra/issues/28))
- Refactoring error messages and endpoint URL paths. ([#40](https://github.com/guilopes15/sabores-da-terra/issues/40))
- Adding and configuring the nginx web server.
- Managing resources and performing load testing with Siege. ([#43](https://github.com/guilopes15/sabores-da-terra/issues/43))
- Adding rate limit on the web server. ([#43](https://github.com/guilopes15/sabores-da-terra/issues/43))
