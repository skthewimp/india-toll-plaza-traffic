# Heavy-vehicle toll crossings in August 2026

The IHMCL report contains 1,247 toll-plaza rows and 337.1 million FASTag
crossings in August 2026. Vehicles with three or more axles account for 65.1
million crossings - 19.3% of the total, or about 2.1 million crossings a day.

## The distribution is skewed, but not dominated by a handful of plazas

The mean plaza recorded 1,683 heavy-vehicle crossings a day; the median was
941. A relatively small group is substantially busier, but this is still a
network story rather than a ten-plaza story. The ten busiest plazas account for
5.6% of heavy crossings, the busiest 50 account for 19.3%, and the busiest 100
account for 32.2%.

Samakhiali led the country with about 16,605 heavy-vehicle crossings a day,
followed by Surajbari at 15,946. Both sit in the Gandhidham PIU. Kishangarh and
Thikariya followed, with roughly 12,824 and 12,000 daily crossings.

## Gujarat and Rajasthan corridors stand out

The Jaipur regional office accounted for 6.7 million heavy crossings, or 10.2%
of the national total. Gandhinagar was close behind at 6.2 million, or 9.6%.
Vijayawada, Bangalore and Bhopal followed. The regional-office field is an NHAI
administrative grouping, not a state field, but it gives a useful first view of
where the busiest freight corridors sit.

## Important limitations

- These are plaza crossing events, not unique trucks. A truck can appear at
  several plazas on one journey and can cross the same plaza more than once.
- The traffic file has no coordinates. Locations must be joined from
  Rajmargyatra, whose plaza names do not always match IHMCL's spelling.
- The supplied map reports locations for 1,109 plazas covering 95% of heavy
  crossings. That appears to be a reviewed matching result rather than a direct
  row count from either source.
- IHMCL warns that transaction data may change after settlement and
  reconciliation. These findings describe the downloaded report, not an
  immutable administrative total.

Run `analysis/summarise_august_2026.py` after downloading and extracting the
source files to reproduce the figures above.
