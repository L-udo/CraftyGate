<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
<img width="804" height="242" alt="craftygate" src="https://github.com/user-attachments/assets/479384e8-eaa2-4b85-9743-af5566bfe9a7" />


  <h3 align="center">CraftyGate</h3>

  <p align="center">
    A poorly written automated Minekube Gate config updater
    <br />
    <a href="https://github.com/user-attachments/assets/3307dbd1-201a-41e9-9ab9-0f97fd230009">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->


<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple python script to automate the creation & updating of the Minekube Gate(Lite Mode Only no bedrock support) config.yml

Here's why:
* I dont know why this doesnt exist already, it's dead simple and not that hard to implement?
* The method of subdomain creation that pterodactyl.io uses is honestly a very weird and cumbersome appoach.
* Removing the reliance on services like cloudflare for subdomain creation, its far easier to use a simple reverse proxy



<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* docker



<!-- USAGE EXAMPLES -->
## Usage

Designed to run in docker compose or as an independent script

**Please ensure Minekube Gate instance is running on the same network/has access to the Crafty instance**



### _All environment variables are required_

docker compose example:
```sh
    craftygate:
        image: almondl/craftygate:latest
        container_name: craftygate
        restart: unless-stopped
        environment:
          - EXTERNAL_PROXY_URL=<gate_proxy_domain>
          - CRAFTY_CONTAINER_HOSTNAME= <root domain/hostname of crafty webui/api>
          - CRAFTY_USERNAME=<crafty_username>
          - CRAFTY_PASSWORD=<crafty_password>
          - STARTING_PORT=20000
    
        volumes:
        - <gate_config_file>:/config.yml
        - <crafty_server_folder:servers/
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Update config file on server removal
- [ ] Better documentation
- [ ] Write it again, but better
- [ ] Rename servers to matching proxy url


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Discord: lvdo

or

submit an issue on this repo


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## libraries usesd

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [jproperties](https://choosealicense.com](https://pypi.org/project/jproperties/))
* [requests](https://www.webpagefx.com/tools/emoji-cheat-sheet](https://pypi.org/project/requests/))
* [ruamel.yaml](https://flexbox.malven.co/](https://pypi.org/project/ruamel.yaml/))
* [tinydb](https://grid.malven.co/](https://pypi.org/project/tinydb/))

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
