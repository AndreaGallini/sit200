/**
 * prevent-back.js
 * 
 * Script da includere nelle pagine da cui non si deve poter tornare indietro.
 * Questo script modifica l'history API del browser per impedire 
 * la navigazione all'indietro e reindirizza l'utente alla pagina
 * operation-not-allowed quando tenta di farlo.
 */

(function() {
    // Aggiungi una voce alla history per impedire di tornare alla pagina precedente
    window.history.pushState(null, "", window.location.href);
    
    // Quando l'utente preme "indietro", intercettalo e reindirizza
    window.onpopstate = function() {
        // Aggiungi di nuovo una voce alla history per impedire di andare indietro
        window.history.pushState(null, "", window.location.href);
        
        // Reindirizza alla pagina operation-not-allowed
        window.location.href = "/operation-not-allowed/";
    };
})(); 