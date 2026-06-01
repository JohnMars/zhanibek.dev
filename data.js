/* Shared site data — articles, talks, etc.
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
      slug: "thinking-in-coroutines",
      title: "Thinking in coroutines, not threads",
      date: "2026-04-22",
      readTime: 9,
      tag: "android",
      excerpt: "After a decade of background-threading patterns on Android, switching mental models took longer than the syntax. Here's what finally clicked.",
      featured: true
    },
    {
      slug: "ci-as-design-tool",
      title: "CI as a design tool",
      date: "2026-03-08",
      readTime: 6,
      tag: "process",
      excerpt: "The pipeline isn't infrastructure. It's the loudest stakeholder in the room — it shapes what shipping feels like.",
      featured: true
    },
    {
      slug: "the-quiet-screen",
      title: "The quiet screen",
      date: "2026-02-14",
      readTime: 4,
      tag: "design",
      excerpt: "A short essay on UI density, attention, and why my favorite Android app has only three buttons."
    },
    {
      slug: "junit-is-not-the-enemy",
      title: "JUnit is not the enemy of fast feedback",
      date: "2026-01-19",
      readTime: 11,
      tag: "testing",
      excerpt: "A common refrain on teams: \"the test suite is slow.\" Almost always, the suite is fine. The seams are wrong."
    },
    {
      slug: "leading-without-becoming-a-manager",
      title: "Leading without becoming a manager",
      date: "2025-12-02",
      readTime: 7,
      tag: "team",
      excerpt: "Notes from three years of staff-IC work — what changed, what stayed quiet, and the specific habits that compounded."
    },
    {
      slug: "small-tools-small-teams",
      title: "Small tools, small teams",
      date: "2025-10-30",
      readTime: 5,
      tag: "process",
      excerpt: "Internal tooling rarely deserves a roadmap. It deserves a Tuesday afternoon."
    }
  ],

  talks: [
    {
      slug: "shape-of-android-modules",
      title: "The shape of Android modules",
      venue: "Berlindroid",
      date: "2025-11-14",
      year: 2025,
      city: "Berlin",
      duration: "32 min",
      featured: true,
      abstract: "Module boundaries are the strongest design tool we have on Android — and most of us are using them as an afterthought. This talk walks through three module shapes I've seen ship, the bugs each one tends to hide, and a pragmatic checklist for choosing between them."
    },
    {
      slug: "ten-years-one-codebase",
      title: "Ten years, one codebase",
      venue: "Droidcon",
      date: "2025-06-28",
      year: 2025,
      city: "London",
      duration: "45 min",
      featured: true,
      abstract: "What does a decade of continuous delivery in a single Android app actually look like? A retrospective on the migrations that worked, the ones that didn't, and the ones that quietly never finished."
    },
    {
      slug: "automating-the-boring-parts",
      title: "Automating the boring parts of release",
      venue: "MobileTech Conf",
      date: "2024-09-19",
      year: 2024,
      city: "Munich",
      duration: "28 min"
    },
    {
      slug: "testing-without-fear",
      title: "Testing without fear",
      venue: "Kotlin Berlin Meetup",
      date: "2024-04-10",
      year: 2024,
      city: "Berlin",
      duration: "20 min"
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
