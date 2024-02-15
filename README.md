# UNSWCourseMap

Deployed [here](https://unsw-course-map.vercel.app/).

## Todo
- [x] Operational course scraper for COMP, SENG and relevant MATH courses
- [x] Add information about terms, course field, etc.
- [x] Evaluate prerequisites as edges and construct graph
- [x] Successfully store in database
- [x] Create flask server for querying database
- [x] Create basic frontend that displays graph
- [ ] Fix bug where a singular course left in a group won't collapse to be a single prereq
- [ ] COMP9301 bug
- [ ] See if there is a way to resume the database if it is paused (if not probably change database)
- [x] Make certain course nodes a bigger scale based on how many people take the course (scrape timetable as well)
- [x] Deploy
- [ ] Update readme with additional information/instructions
- [ ] Improve styling of code (mostly for react code)
- [ ] Generally make frontend more appealling
- [X] Colour code nodes on subject area
- [ ] Test using GPT API to get a more accurate read on subject area (as opposed to the handbook)
- [ ] Enabled/disable different terms
- [X] Hover on node for additional information (maybe a modal with a link to course page)
- [X] Add link to course page (update db) and also remove annoying prereq text before prereq
- [X] Added link to unielectives page
- [ ] 'Show me a random course' button
- [ ] Add other courses (eg COMM, ARTS, etc); maybe enabled which ones you want
- [ ] Add postgraduate option
- [ ] Add any mark prerequisites as edges on the graph
- [ ] Hover on nodes to view prereqs
- [ ] Find better colours for node fields


