let fs = require("fs");
jsonFile = fs.readFileSync("matchsToDay.json");
let matchs = JSON.parse(jsonFile);
// console.log(matchs.length)

stats = {
  matchCountByDay: {},
  matchCountByLeague: {},
  matchCountByCountry: {},
};

days = [...new Set(matchs.map((match) => match.Day))];
leagues = [...new Set(matchs.map((match) => match.league))];
countries = [...new Set(matchs.map((match) => match.country))];

days.forEach((element) => {
  stats.matchCountByDay[element] = matchs.filter(
    (match) => (match.Day == element)
  ).length;
});
leagues.forEach((element) => {
  stats.matchCountByLeague[element] = matchs.filter(
    (match) => (match.league == element)
  ).length;
});
countries.forEach((element) => {
  stats.matchCountByCountry[element] = matchs.filter(
    (match) => (match.country == element)
  ).length;
});


console.log(stats)
// matchs.filter((match)=>match.league=="Bundesliga").forEach((match)=>{
//     console.log("Bundesliga Match")
//     console.log(`Day : ${match.Day}`)
//     console.log(`${match.home} VS ${match.away} `)
// })