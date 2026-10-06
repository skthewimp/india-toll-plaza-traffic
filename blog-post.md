# The toll-plaza map had a source line. Finding the actual data was messier.

I started with a map of heavy-truck traffic across India. It had the useful kind
of source note: IHMCL FASTag data for August 2026, with locations from NHAI's
Rajmargyatra list. That sounds like a two-download job.

It was not quite a two-download job.

The IHMCL page labels the August link as an Excel file, but serves a ten-page
PDF. The PDF contains 1,247 toll plazas and six vehicle classes. Rajmargyatra,
meanwhile, exposes the location data through an API. The two sources do not
share clean, stable plaza names. The map reports 1,109 located plazas covering
95% of heavy crossings, which is a clue that somebody did a reasonably careful
matching exercise in between.

I downloaded the full public trail while I was there: every monthly
vehicle-class report from January 2022 through August 2026, the related MLFF and
annual-pass reports, the current Rajmargyatra response, and a few dated location
snapshots. The download is about 79 MB. None of it is in the GitHub repository.

That separation is deliberate. Government source files can be revised, their
reuse terms are not the same as the code's, and a repo full of PDFs is not
especially helpful anyway. The repo contains the downloader, PDF extractor,
location exporter, analysis code, and notes. Run the scripts and the data stays
local.

The first result is straightforward but useful. India recorded 65.1 million
FASTag crossings by vehicles with three or more axles in August - about 2.1
million a day. Samakhiali and Surajbari were the two busiest plazas. The traffic
is skewed, although not as concentrated as I expected: the busiest ten plazas
account for only 5.6% of heavy crossings.

The awkward part is still the join. Names drift between systems, punctuation is
inconsistent, and a fuzzy match that looks plausible can put a toll plaza in the
wrong place. I have left that as an explicitly reviewed step rather than hiding
it inside an overconfident string-matching function.

The code and notes are here: <https://github.com/skthewimp/india-toll-plaza-traffic>

PS: crossings are not trucks. One truck driving through five plazas contributes
five observations. That distinction is easy to lose once the circles appear on
a map.
