    var matchInfo = {
      "rounds" : [
        { "name": "Round1",
          "matches" : [
            { "id" : 1, "p1" : "mTwDeMuslim", "p2" : "Luffy" },
            { "id" : 2, "p1" : "SeleCT", "p2" : "NEXGenius" },
            { "id" : 3, "p1" : "Fenix", "p2" : "SoftBall" },
            { "id" : 4, "p1" : "White-Ra", "p2" : "Ice" },
            { "id" : 5, "p1" : "HuK", "p2" : "RedArchon" },
            { "id" : 6, "p1" : "Capoch", "p2" : "Loner" },
            { "id" : 7, "p1" : "mTwDIMAGA", "p2" : "MakaPrime" },
            { "id" : 8, "p1" : "TLAF-Liquid`TLO", "p2" : "SEN" }
          ]
        },
        { "name": "Round2",
          "matches" : [
            { "id" : 9, "p1" : null, "p2" : null },
            { "id" : 10, "p1" : null, "p2" : null },
            { "id" : 11, "p1" : null, "p2" : null },
            { "id" : 12, "p1" : null, "p2" : null }
          ]
        },
        { "name": "Round3",
          "matches" : [
            { "id" : 13, "p1" : null, "p2" : null },
            { "id" : 14, "p1" : null, "p2" : null },
          ]
        },
        { "name": "Round4",
          "matches" : [
            { "id" : 15, "p1" : null, "p2" : null },
          ]
        } 
      ]
    };
  
    $(document).ready(function($) {       
      var base = $('#writeHere');
      var matchDivsByRound = [];
      
      for (var roundIndex=0; roundIndex<matchInfo.rounds.length; roundIndex++) {    
        var round = matchInfo.rounds[roundIndex];
        var bracket = checkedAppend('<div class="bracket"></div>', base);
        var matchDivs = [];
        matchDivsByRound.push(matchDivs);
        
        //setup the match boxes round by round
        for (var i=0; i<round.matches.length; i++) {                     
          var vOffset = checkedAppend('<div></div>', bracket);
        
          var match = round.matches[i];
          var matchHtml = '<div class="match" id="match' + match.id + '">'
            + '<div class="p1">' + fmtName(match.p1) + '</div>'
            + '<div class="spacer"></div>'
            + '<div class="p2">' + fmtName(match.p2) + '</div>';
          matchDiv = checkedAppend(matchHtml, bracket);
          matchDivs.push(matchDiv);
          
          if (roundIndex > 0) {
            //row 2+; line up with previous row
            var alignTo = matchDivsByRound[roundIndex-1][i*2];
            //offset to line up tops
            var desiredOffset = alignTo.position().top - matchDiv.position().top;
            
            //offset by half the previous match-height
            desiredOffset += alignTo.height() / 2;
            vOffset.height(desiredOffset);            
          } else {
            checkedAppend('<div class="small-spacer"></div>', bracket);
          }
          
          if (roundIndex > 0) {
            //tweak our size so we stretch to the middle of the appropriate element
            var stretchTo = matchDivsByRound[roundIndex-1][i*2+1];
            var newH = stretchTo.position().top + stretchTo.height()/2 - matchDiv.position().top;            
            var deltaH = newH - matchDiv.height();
            matchDiv.height(newH);
            var spacer = matchDiv.find('.spacer');
            spacer.height(spacer.height() + deltaH);
          }          
        }                
      }
      //setup the final winners box; just a space for a name whose bottom is centrally aligned with the last match
      bracket = checkedAppend('<div class="bracket"></div>', base);
      var vOffset = checkedAppend('<div></div>', bracket);
      var alignTo = matchDivsByRound[matchInfo.rounds.length - 1][0]; //only 1 match in the last round
      var html = '<div class="winner">?</div>';
      var winnerDiv = checkedAppend(html, bracket);      
      vOffset.height(alignTo.position().top - winnerDiv.position().top + alignTo.height() / 2 - winnerDiv.height());
    });
    
    function fmtName(name) {
      return null != name ? name : '?';
    }
    
    function checkedAppend(rawHtml, appendTo) {
      var html = $(rawHtml);
      if (0 == html.length) {
        throw "Built ourselves bad html : " + rawHtml;
      }
      html.appendTo(appendTo);      
      return html;
    }
