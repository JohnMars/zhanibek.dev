/* Shared site data - articles, talks, etc.
   Used by index, articles, talks pages and search.
   Exposed on window.SITE.
*/
window.SITE = {
  author: {
    name: "Zhanibek Marshal",
    role: "Android engineer · speaker · writer",
    bio: "Professional Android developer with over 10 years of experience. Active in the dev community, speaker at Berlindroid and other conferences. Believer in clean, testable code and automated process.",
    location: "Berlin",
    links: {
      linkedin: "https://www.linkedin.com/in/johnmarshal/",
      mastodon: "https://androiddev.social/@zhanibek",
      rss: "feed.xml",
      email: "mailto:hello@zhanibek.dev"
    }
  },

  articles: [
    {
      slug: "state-of-android-at-tr-2024",
      title: "State of Android at Trade Republic - 2024 edition",
      date: "2025-03-10",
      readTime: 10,
      tag: "android",
      excerpt: "A complete overview of Trade Republic's Android stack: Jetpack Compose, MVVM, Kotlin Coroutines, 92% unit test coverage, 800+ regression test cases, and a 40% local build improvement.",
      url: "https://engineering.traderepublic.com/state-of-android-at-tr-2024-edition-bc032620b83e",
      featured: true
    },
    {
      slug: "why-berlin-over-tokyo",
      title: "Почему выбрал Берлин вместо Токио",
      date: "2020-10-11",
      readTime: 18,
      tag: "life",
      excerpt: "Год планировал переехать в Токио, но выбрал Берлин - о трудоголизме, жилье, work-life balance и жизни в немецкой столице.",
      url: "why-berlin-over-tokyo.html"
    },
    {
      slug: "farewell-kolesa",
      title: "Farewell Kolesa Group",
      date: "2019-05-31",
      readTime: 2,
      tag: "career",
      excerpt: "After 4 years and 3 months at the best IT company in Kazakhstan, moving on - and what leading an Android team taught me about staying kind.",
      url: "farewell-kolesa.html"
    },
    {
      slug: "kolesa-academy-android",
      title: "Колёса Академия - что нужно знать Android разработчику",
      date: "2018-12-08",
      readTime: 12,
      tag: "android",
      excerpt: "OOP, паттерны, алгоритмы и Android SDK - что нужно знать, чтобы пройти отбор в Колёса Академию.",
      url: "kolesa-academy-android.html"
    },
    {
      slug: "android-architecture-components-codelab",
      title: "Code Labs: Android Architecture Components",
      date: "2018-10-12",
      readTime: 25,
      tag: "android",
      excerpt: "Пошаговый codelab с DevFest Almaty 2018: ViewModel, LiveData, Room и Repository - строим приложение-клон Колёс.",
      url: "android-architecture-components-codelab.html"
    },
    {
      slug: "why-android-kotlin-ru",
      title: "Почему Android разработчики переходят на Kotlin",
      date: "2018-09-28",
      readTime: 1,
      tag: "android",
      excerpt: "Заметки с митапа DrinkUp Almaty о прелестях Kotlin и почему разработчики уходят с Java.",
      url: "why-android-kotlin-ru.html"
    },
    {
      slug: "modular-android-libraries-ru",
      title: "Модульная разработка Android приложений",
      date: "2018-04-20",
      readTime: 2,
      tag: "android",
      excerpt: "Как «Колёса Крыша Маркет» вынесла бизнес-логику и слой данных в общую библиотеку для трёх продуктов.",
      url: "modular-android-libraries-ru.html"
    },
  ],

  talks: [
    {
      slug: "maestro-reliable-e2e-testing-made-easy",
      title: "Maestro: Reliable E2E testing made easy",
      venue: "Droidcon Berlin",
      date: "2025-10-01",
      year: 2025,
      city: "Berlin",
      duration: "30 min",
      featured: true,
      slides: "https://speakerdeck.com/johnmars/maestro-reliable-e2e-testing-made-easy",
      video: "https://www.youtube.com/watch?v=aVCyYMkOrf0",
      thumbnail: "assets/thumbnails/maestro-e2e-maxres.jpg",
      photos: ["assets/thumbnails/maestro-reliable-e2e-testing-made-easy.jpg", "assets/thumbnails/maestro-e2e-frame0.jpg"],
      abstract: "End-to-end tests are often brittle, slow, and painful to maintain. But what if you could write E2E tests as easily as user stories, run them locally and in CI, and skip the flaky UI tests that break on every layout change? In this talk, I walk you through how Maestro, an open-source mobile UI testing framework, is reshaping the way we think about mobile E2E testing - setting it up in under 5 minutes, writing human-readable flows, integrating with CI, and gaining confidence in critical user journeys from login to money transfer."
    },
    {
      slug: "maestro-ui-testing-framework",
      title: "Maestro - UI Testing Framework",
      venue: "GDG Berlin Android",
      date: "2023-10-11",
      year: 2023,
      city: "Berlin",
      duration: "30 min",
      featured: true,
      slides: "https://speakerdeck.com/johnmars/maestro-ui-testing-framework",
      thumbnail: "assets/thumbnails/maestro-ui-testing-framework.jpg",
      abstract: "The talk discussed the implementation of Maestro UI testing framework to address the challenge of time-consuming regression testing across Android and iOS platforms. This talk showcased how Maestro streamlined the regression testing process, enhancing efficiency and test coverage across platforms."
    },
    {
      slug: "design-system-driven-android-development-a-guide-to-automation-tools",
      title: "Design System Driven Android Development: A Guide to Automation Tools",
      venue: "Droidcon Berlin",
      date: "2023-08-02",
      year: 2023,
      city: "Berlin",
      duration: "30 min",
      featured: true,
      slides: "https://speakerdeck.com/johnmars/design-system-driven-android-development-a-guide-to-automation-tools",
      thumbnail: "assets/thumbnails/design-system-driven-android-development.jpg",
      abstract: "How Trade Republic automates design system work on Android: Figma asset export, snapshot testing with Paparazzi, and KSP-based annotation tools to keep components consistent across devices."
    },
    {
      slug: "android-kz-meetup-jetpack-compose-navigation",
      title: "Jetpack Compose Navigation",
      venue: "Android KZ Meetup",
      date: "2022-08-06",
      year: 2022,
      city: "Online",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/android-kz-meetup-jetpack-compose-navigation",
      thumbnail: "assets/thumbnails/android-kz-meetup-jetpack-compose-navigation.jpg",
      abstract: "The evolution of Android navigation - from Activity/Intent through Fragment Manager to Jetpack Navigation in Compose - with practical NavHost and navigation graph demos."
    },
    {
      slug: "kak-v-21-ghodu-stat-android-razrabotchikom",
      title: "How to Become an Android Developer in 2021",
      venue: "Online talk",
      date: "2021-11-05",
      year: 2021,
      city: "Online",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/kak-v-21-ghodu-stat-android-razrabotchikom",
      thumbnail: "assets/thumbnails/kak-v-21-ghodu-stat-android-razrabotchikom.jpg",
      abstract: "A roadmap for developers entering Android in 2021: tracing the platform's evolution and the tools, languages, and architecture patterns that actually matter."
    },
    {
      slug: "po-chiesnoku-o-bizniesie-ili-zachiem-nam-nuzhien-domain-layer",
      title: "Why We Need a Domain Layer",
      venue: "Android meetup",
      date: "2019-11-30",
      year: 2019,
      city: "Almaty",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/po-chiesnoku-o-bizniesie-ili-zachiem-nam-nuzhien-domain-layer",
      thumbnail: "assets/thumbnails/po-chiesnoku-o-bizniesie-domain-layer.jpg",
      abstract: "Clean Architecture in practice: identifying business logic, understanding use cases, and building a domain layer that stays independent of UI and data concerns."
    },
    {
      slug: "uluchshaiem-zhizn-android-razrabotchika-s-kotlin-coroutines-i-viewmodel",
      title: "Improving Android Developer Life with Kotlin Coroutines and ViewModel",
      venue: "Kolesa-conf",
      date: "2019-04-12",
      year: 2019,
      city: "Almaty",
      duration: "25 min",
      slides: "https://speakerdeck.com/johnmars/uluchshaiem-zhizn-android-razrabotchika-s-kotlin-coroutines-i-viewmodel",
      thumbnail: "assets/thumbnails/uluchshaiem-zhizn-kotlin-coroutines-viewmodel.jpg",
      abstract: "Using ViewModel and stable Kotlin Coroutines to implement MVVM and handle async work - reducing complexity and flattening the learning curve for new team members at Kolesa."
    },
    {
      slug: "novyi-urovien-modul-noi-razrabotki-mon-repo",
      title: "A New Level of Modular Development: Mono Repo",
      venue: "Internal tech talk",
      date: "2018-11-24",
      year: 2018,
      city: "Almaty",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/novyi-urovien-modul-noi-razrabotki-mon-repo",
      thumbnail: "assets/thumbnails/novyi-urovien-modul-noi-razrabotki-mon-repo.jpg",
      video: "https://www.youtube.com/watch?v=rfdfUxqXaMc",
      abstract: "How Kolesa Team evolved from separate repos through Git submodules to a monorepo - streamlining their workflow and enabling large-scale architectural changes across four apps."
    },
    {
      slug: "ot-teorii-do-testirovaniya-mvvm",
      title: "From Theory to Testing MVVM",
      venue: "Kolesa Meetup",
      date: "2019-06-01",
      year: 2019,
      city: "Almaty",
      duration: "30 min",
      video: "https://www.youtube.com/watch?v=9xMZrHXBcFI",
      thumbnail: "assets/thumbnails/mvvm-testing-talk.jpg",
      abstract: "From architectural theory to practical MVVM testing - separating ViewModel and View concerns, writing unit-testable business logic, and applying LiveData and fake repositories in real Kolesa codebase examples."
    },
    {
      slug: "pochiemu-android-razrabotchiki-pieriekhodiat-na-kotlin",
      title: "Why Android Developers Switch to Kotlin",
      venue: "DrinkUp Almaty",
      date: "2018-08-23",
      year: 2018,
      city: "Almaty",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/pochiemu-android-razrabotchiki-pieriekhodiat-na-kotlin",
      thumbnail: "assets/thumbnails/pochiemu-android-razrabotchiki-kotlin.jpg",
      abstract: "Kotlin's key features - null safety, smart casts, data classes, lambdas - and why they solve Java's common pain points, with side-by-side code comparisons."
    },
    {
      slug: "posliedovatiel-no-o-paralliel-nosti-v-android",
      title: "Concurrency in Android: A Sequential Guide",
      venue: "Kolesa.Mobile 1.0",
      date: "2016-12-03",
      year: 2016,
      city: "Almaty",
      duration: "20 min",
      slides: "https://speakerdeck.com/johnmars/posliedovatiel-no-o-paralliel-nosti-v-android",
      thumbnail: "assets/thumbnails/posliedovatiel-no-paralliel-nost-android.jpg",
      abstract: "Why parallelism matters on Android, the main UI thread's role, and a practical comparison of Thread, AsyncTask, HandlerThread, and Loader - with notes on avoiding memory leaks."
    }
  ]
};

/* helpers */
window.SITE.fmtDate = (iso) => {
  const d = new Date(iso);
  return d.toLocaleDateString("en-GB", { year: "numeric", month: "short", day: "numeric" }).toLowerCase();
};
window.SITE.fmtMonthYear = (iso) => {
  const d = new Date(iso);
  return d.toLocaleDateString("en-GB", { year: "numeric", month: "short" }).toLowerCase();
};
