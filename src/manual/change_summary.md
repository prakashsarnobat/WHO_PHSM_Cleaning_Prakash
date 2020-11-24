Change summary 2020-11-24

* US Virgin Islands recorded as country, not US state


* New OXCGRT "no update" phrases


* Prevent CDC country from being present in area_covered


  Chris: You said in the call that all CDC records should be set to national but this week we had an issue where all CDC records were set to "other" (probably why it looked like all of the other records were actually national?) I have left it so that CDC admin_level flag == Subnational/regional only will be converted to "other" and and area_covered will be blank
  From looking at a few - this seems to be the correct approach to me.


* For ACAPS, where targeted = 'checked', 'Checked', 'general', or 'General': targeted is set to blank

* For ACAPS: where area_covered is blank admin_level fixed to be 'national'
  * Was affecting a few records with a hidden space in admin_level

* For JH_HIT: when comment and link is blank, code as who_code == 11

* For OXCGRT records with a "no update" phrase - retain these records but code as who_code == 10

* Set Occupied Palestine including East Jerusalem to an admin region of Israel.

* Added check for violations of the (one way) one-to-one relationship between:
  * ISO and who_region
  * ISO and iso_3166_1_numeric
  * ISO and country_territory_area
