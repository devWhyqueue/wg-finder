from wgfinder.chatgpt import summarize_flat_ad

flat_description = (
    "Hallo ihr Suchenden,\n\n"
    "unsere liebe Mitbewohnerin zieht mit ihrem Freund in eine eigene Wohnung, somit wird das Zimmer frei.\n\n"
    "Nichtraucherwohnung, Altbau, hohe Decken, Erdgeschoss - EG, ruhige Seitenstraße.\n\n"
    "Möbliert, Hochbett, Schreibtisch, Stühle, 2-er Sofa, Sessel, Kleiderschrank, Kommode.\n"
    "Kann man alles benutzen oder ihr bringt komplett eigene Möbel mit, dann kommen die hier vorhandenen Möbel weg.\n\n"
    "Anmeldung natürlich möglich.\n\n"
    "Sonst alles da, Wasch- u. Spülmaschine, voll eingerichtete Küche usw.\n\n"
    "Liebe Grüße,\n"
    "Tom\n"
    "----------------------------------------------------------------------------------------------------------------------\n"
    "ENGLISH\n\n"
    "Hi guys,\n\n"
    "our dear flatmate moves into an own appartement together with her boyfriend, so the room is free.\n\n"
    "ONLY for grown up, responsible people who know how to run a household and keep the bathroom and kitchen clean. "
    "If you can´t do that, you´re very wrong here.\n\n"
    "Non-smoker flat. \"Altbau\" = apartment in old building. Flat is on the ground floor. House is in a smal, quiet street, "
    "has a big bathroom and kitchen.\n"
    "Of course you can use the washing-machine and kitchen etc.\n\n"
    "Yes, you can get a tenancy/sublease (Untermietvertrag) and a \"Anmeldung\" = registration.\n\n"
    "There´s furniture like a bed, desk, wardrobe (closet), some chairs, sofa/couch, if you need it. "
    "If not, you can bring your own furniture, then the furniture from this room will be removed.\n\n"
    "Good connection to public transport.\n\n"
    "I´m a cinematographer and photographer, I like to do some sports (no fitnessfreak), play some piano - "
    "but at home only E-Piano with headphones, so you don´t hear anything. Your other flatmate would be a very open minded IT-guy, "
    "very communicative an interested in many things.\n\n"
    "Great if you already have experience with living in a shared-flat.\n\n"
    "We have a relaxed life here, sometimes we talk/eat/drink together in the kitchen. Or not, then we chill or work alone in our own room. "
    "There´s no \"must\" for anything.\n\n"
    "Späti (late-shop) and supermarket 3 min. away.\n"
    "Public transport:\n"
    "ca. 3 min to tram (50, M13).\n"
    "ca. 4 min to S-Bahn Bornholmer Straße (S1, S2, S25, S26, S8, S85)\n"
    "ca. 12 min to U/S-Bahn (subway) Schönhauser Allee (U2, S8, Ringbahn S41, S42)\n\n"
    "Best,\n"
    "Tom"
)


def test_summarize_flat_ad():
    response = summarize_flat_ad(flat_description)
    print(response)
