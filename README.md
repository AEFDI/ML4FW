# ML4FW-Fragebogen - Eine Bewertungsmethode für Machine Learning Use Cases im Betrieb von Fernwärmenetzen

Dieses Repositorium enthält den Sourcecode für eine Python-Anwendung zur Bewertung von 
Machine Learning (ML) Use Cases im Bereich des Fernwärmenetzbetriebs hinsichtlich Nutzen, Aufwand und Risiko. 
Dabei wird dem Nutzer innerhalb eines Fragebogens ermöglicht in ca. 15 min bis zu 19 ausgewählte ML Use Cases in bis 
zu 5 Kategorien zu bewerten. Durch die Kombination der Antworten des Anwenders mit dem hinterlegtem 
Hintergrundwissen wird eine Bewertung auf einer Skala von 1 bis 5 hinsichtlich der Größen Nutzen, Aufwand und Risiko 
erstellt und grafisch dargestellt. Der Nutzer nimmt im Rahmen des Fragebogens eine subjektive Gewichtung der 
Bewertungskriterien vor und bringt auf diese Weise seine individuelle Perspektive mit ein. Damit ermöglicht die 
grafische Aufbereitung der Bewertungsergebnisse dem Nutzer eine auf ihn abgestimmte erste Priorisierung von ML Use 
Cases vorzunehmen und erleichter somit den Einstieg in tiefergehende Analysen von ML Use Cases mit Potenzial.

# Inhaltsverzeichnis

- [Installation / Anleitung](#installation--anleitung)
- [Hintergrund](#hintergrund)
- [Methodik](#methodik)
  - [Kategorieauswahl](#kategorieauswahl)
  - [Gewichtung der globalen Kriterien](#gewichtung-der-globalen-kriterien)
  - [Beantwortung kategorieübergreifender Fragen](#beantwortung-kategorieübergreifender-fragen)
  - [Gewichtung der lokalen Kriterien](#gewichtung-der-lokalen-kriterien)
  - [Beantwortung kategoriespezifischer Fragen](#beantwortung-kategoriespezifischer-fragen)
  - [Auswertung der Angaben](#auswertung-der-angaben)
  - [Ergebnisdarstellung](#ergebnisdarstellung)
- [Abgebildete ML Use Cases](#abgebildete-ml-use-cases)
- [Lizenz](#lizenz)

# Installation / Anleitung
Für die Anwendung des ML4FW-Fragebogens gibt es 4 mögliche Wege:

## 1. Download der 'ML4FW_Fragebogen.exe' aus diesem Repositorium.
Vorteil: Die Anwendung kann durch einen einfachen Doppelklick gestartet werden.
Nachteil: Die Anwendung benötigt eine lange Zeit zum Starten.

## 2. Download des 'ML4FW_Fragebogen.zip' Verzeichnisses
Das 'ML4FW_Fragebogen.zip'-Verzeichnis enthält zusätzlich zur 'ML4FW_Fragebogen.exe' einen '_internal'-Ordner. Durch das
Entpacken des Verzeichnisses und das Ausführen der exe-Datei innerhalb des Verzeichnisses wird der Startvorgang der
Anwendung erheblich beschleunigt.

Vorteile: 
    - Schnellerer Startvorgang.
Nachteile: 
    - Komplizierter als einfacher exe-Download.
    - Nutzung unter Linux ist nicht möglich.

## 3. Ausführen von 'ML4FW_Fragebogen.py'
Nach dem Klonen des Repositoriums via git und dem Installieren der benötigten [Packages](./requirements.txt) 
(bspw. durch `pip install -r requirements.txt`), kann die Datei 'ML4FW_Fragebogen.py' gestartet werden.
Dafür wird die Python Version [3.10.10](https://www.python.org/downloads/release/python-31010/) benötigt.

Vorteile: 
    - Mehr Kontrolle über den Ausführungsprozess und Modifikation von python-Dateien ist möglich. 
    - Ausführung auf Linux ist möglich.
Nachteile: 
    - Installation von Python und grundlegende Python-Kenntnisse sind notwendig.

## 4. Erstellen einer eigenen exe-Datei
Analog zu Möglichkeit 3 kann nach der Einrichtung einer Python-Umgebung eine eigene exe-Datei erstellt werden.
Dafür kann bspw. das Python-Package [pyinstaller](https://pyinstaller.org/en/stable/) genutzt werden. Zum Erstellen der einfachen exe-Datei aus Schritt 1
kann der Befehl `pyinstaller --onefile --noconsole --add-data "data;data" --hidden-import "ml4fw_fragebogen" ML4FW_Fragebogen.py` genutzt werden.
Für Variante 2 kann der Befehl `pyinstaller --onedir --noconsole --add-data "data;data" --hidden-import "ml4fw_fragebogen" ML4FW_Fragebogen.py` verwendet 
werden.

Vorteil: 
    - Erstellung der exe-Datei auf Linux ist möglich.
Nachteil: 
    - Pyinstaller oder ein ähnliches Tool wird zusätzlich benötigt.

# Hintergrund

Der ML4FW Fragebogen wurde vollständig im Rahmen der wissenschaftlichen Begleitung des Projekts ML4FW - 
Erprobung eines Use Cases für den Einsatz von Machine Learning im Fernwärmenetzbetrieb - im Auftrag der 
Deutschen Energie-Agentur GmbH (dena) entwickelt. 

# Methodik 

Die Bewertung von ML Use Cases im Fernwärmenetzbetrieb findet durch eine Kombination von Nutzerpräferenzen, den 
Umgebungsbedingungen des Nutzers und Hintergrundwissen aus durchgeführten Literaturrecherchen, Umfragen und 
Expertenmeinungen statt. Die notwendigen Nutzerinformationen werden im Rahmen eines Fragebogens erhoben, der sich 
in die Schritte Kategorieauswahl, Gewichtung der globalen (kategorieübergreifende) Kriterien, kategorieübergreifender Fragen, 
Gewichtung der lokalen (kategoriespezifischen) Kriterien und kategoriespezifische Fragen. Anschließend werden 
die Nutzerangaben im Kontext des Hintergrundwissens ausgewertet und visualisiert.

## Kategorieauswahl

Der Nutzer wählt die für ihn relevanten ML Use Case-Kategorien aus den fünf Kategorien Wärmebedarfsprognosen (WBP), 
Instandhaltung Hausstationen (InHAST), Instandhaltung Rohrleitungsnetz (InRN), 
Betriebsstrategien Wärmenetz (BeWN) und Betriebsstrategien Hausstation (BeHAST) aus.

## Gewichtung der globalen Kriterien

Der Nutzer nimmt eine subjektive Gewichtung der drei globalen Aufwandskriterien Kostenaufwand, Zeitaufwand, 
Personalaufwand und der vier Nutzen-Kriterien Versorgungssicherheit, Umweltauswirkungen, Automatisierungsgrad und 
Energieeffizienz vor, indem jedem Kriterium eine Zahl von 1 (niedrige Priorität) bis 5 (hohe Priorität) zugewiesen wird. 
Auf diese Weise fließen die individuellen Voraussetzungen des Nutzers in die Bewertung der ML Use Case-Kategorien ein.

## Beantwortung kategorieübergreifender Fragen

Im nächsten Schritt beantwortet der Nutzer Fragen zu Datenverfügbarkeiten und Datenqualität, die für die Bewertung
von Use Cases in vielen oder sogar allen Kategorien relevant sind.

## Gewichtung der lokalen Kriterien

Der Nutzer nimmt für jede der ausgewählten Kategorien eine subjektive Gewichtung der lokalen Nutzen-Kriterien vor. 
Diese Gewichtungen geschehen analog zur Gewichtung der globalen Kriterien. Diese Gewichtung bringt die Perspektive des 
Nutzers in die Bewertung des Nutzens von ML Use Cases innerhalb der jeweiligen Kategorie ein. Eine Auflistung aller
lokalen Kriterien jeder Kategorie findet sich in der folgenden Tabelle:

### Lokale Nutzen-Kriterien
| Kriterium                                 | Beschreibung                                                                                                                                                                                                                                                                       | Kategorie         |
|-------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| Genauigkeit                               | Beschreibt wie gering der Vorhersagefehler bei der Wärmebedarfsprognose voraussichtlich sein wird.                                                                                                                                                                                 | WBP               |
| Interpretierbarkeit                       | Beschreibt die Interpretierbarkeit und Transparenz der erstellen Prognose. Es gibt ML-Ansätze, wie bspw. klassische neuronale Netze, die als Black Box fungieren und damit nur schwer zu interpretieren sind.                                                                   | WBP               |
| Kundenkomfort                             | Beschreibt wie viel Wert auf explizite Berücksichtigung des Kundenkomforts bei der Erstellung von Wärmebedarfsprognosen gelegt wird.                                                                                                                                               | WBP               |
| Fehlererkennung                           | Beschreibt die Fähigkeit des ML-Modells, vorhandene Fehler zu erkennen.                                                                                                                                                                                                             | InHAST            |
| Identifikation von Ursachen               | Beschreibt die Fähigkeit des ML-Modells, Ursachen zu detektierten Fehlern zu identifizieren.                                                                                                                                                                                        | InHAST            |
| Wenige Fehlalarme                         | Beschreibt wie gering die Fehlalarmrate des ML-Modells ist. Bei einem Fehlalarm gibt das ML-Modell an einen Fehler oder eine Anomalie detektiert zu haben, während sich das überwachte System im Normalzustand befindet.                                                           | InHAST            |
| Fehlerfrüherkennung                       | Beschreibt die Fähigkeit des ML-Modells, Fehler bereits in der Entstehung (d. h. bevor sie kritisch für den Betrieb werden) zu detektieren.                                                                                                                                         | InHAST            |
| Interpretierbarkeit                       | Beschreibt die Interpretierbarkeit und Transparenz der Modelle mit Hinsicht auf erkannte Fehler oder Anomalien. Es gibt ML-Ansätze, wie bspw. klassische Autoencoder, die als Black Box fungieren und damit nicht ohne Zusatzaufwand interpretierbar sind.                      | InHAST            |
| Erkennen von vorhandenen Leckagen         | Beschreibt die Fähigkeit des ML-Modells, vorhandene Leckagen zu erkennen.                                                                                                                                                                                                           | InRN              |
| Ortung von Leckagen                       | Beschreibt die räumliche Genauigkeit der Lokalisierung von erkannten Leckagen im Rohleitungsnetz.                                                                                                                                                                                  | InRN |
| Vorbeugung von Fehlern                    | Beschreibt die Fähigkeit des ML-Modells, Leckagen oder Schwachstellen in einem frühen Stadium zu erkennen, bevor diese kritisch für den Betrieb werden.                                                                                                                             | InRN |
| Wenige Fehlalarme                         | Beschreibt wie gering die Fehlalarmrate des ML-Modells ist. Bei einem Fehlalarm gibt das ML-Modell an einen Fehler oder eine Anomalie detektiert zu haben, während sich das überwachte System im Normalzustand befindet.                                                           | InRN |
| Interpretierbarkeit                       | Beschreibt die Interpretierbarkeit und Transparenz der Modelle mit Hinsicht auf erkannte Leckagen. Es gibt ML-Ansätze, die als Black Box fungieren und nur schwer zu interpretieren sind. Andere Modelle benötigen dafür aber oftmals mehr Daten oder sind schwerer anzuwenden. | InRN |
| Energieeffizienz                          | Beschreibt den potenziell positiven Einfluss des ML Use Cases auf die Energieeffizienz des Wärmenetzes.                                                                                                                                                                            | BeWN |
| Interpretierbarkeit                       | Beschreibt die Interpretierbarkeit und Transparenz der Modelle mit Hinsicht auf die getroffenen Entscheidungen. Es gibt ML-Ansätze, die als Black Box fungieren und nur schwer zu interpretieren sind.                                                                          | BeWN |
| Kundenkomfort                             | Beschreibt zu diem Grad Kundenkomfort bei der Erstellung von Netzbetriebsstrategien berücksichtigt wird.                                                                                                                                                                        | BeWN |
| Reduktion der Rücklauftemperatur          | Beschreibt den potenziell positiven Einfluss des ML Use Cases auf die Senkung der Rücklauftemperatur der HAST.                                                                                                                                                                     | BeHAST |
| Interpretierbarkeit                       | Beschreibt die Interpretierbarkeit und Transparenz der Modelle mit Hinsicht auf die getroffenen Entscheidungen. Es gibt ML-Ansätze, die als Black Box fungieren und nur schwer zu interpretieren sind.                                                                          | BeHAST |
| Kundenkomfort                             | Beschreibt zu welchem Grad Kundenkomfort bei der Erstellung von HAST-Betriebsstrategien berücksichtigt wird.                                                                                                                                                                       | BeHAST |

## Beantwortung kategoriespezifischer Fragen

Auf die Gewichtung der lokalen Kriterien folgen die kategoriespezifischen Fragen zum Risiko und Aufwand von ML Use Cases. 
Zunächst werden die Risikofragen gestellt und anschließend Fragen zur Datenverfügbarkeit und potenziellen Datenerhebungs- 
und Datenspeicherungsaufwänden. Jede der gestellten Aufwandsfragen zahlt jeweils auf eines der sieben Aufwandskriterien 
Datenaufbewahrungsaufwand, kontinuierlicher Aufwand, Rechenaufwand, Sensorinstallationsaufwand, Implementationsaufwand, 
Datenerhebungsaufwand und Metadatenerhebungsaufwand ein. Diese Kriterien werden für die Schätzung des Gesamtaufwands 
von Use Cases verwendet.

### Lokale Aufwandskriterien
| Kriterium                       | Beschreibung                                                                          |
|---------------------------------|---------------------------------------------------------------------------------------|
| Datenaufbewahrungsaufwand       | Einschätzung zum benötigten Aufwand für die Datenspeicherung und Datenpflege.         |
| Kontinuierlicher Aufwand         | Schätzung des ständigen Aufwands bei einem kontinuierlichen Betrieb des ML Use Cases. |
| Rechenaufwand                   | Einschätzung des Rechenaufwands, der zur Modellerstellung benötigt wird.              |
| Sensorinstallationsaufwand       | Aufwand bei der Installation neuer Sensorik.                                          |
| Implementationsaufwand          | Aufwand bei der Implementieren der ML-Lösung.                                         |
| Datenerhebungsaufwand           | Aufwand für das Sammeln von Daten für ein Modelltraining.                             |
| Metadatenerhebungsaufwand       | Aufwand für das Sammeln von Metadaten für die Modellierung im Rahmen des Use Cases.   |

## Auswertung der Angaben

Nach der Beantwortung aller Fragen folgt die Auswertung der angegebenen Informationen. Dabei werden Nutzen, Aufwand und 
Risiko der ML Use Case Kategorien evaluiert und semi-quantitativ auf einer Skala von 1 bis 5 eingeordnet. Für 
ML Use Cases wird zunächst geprüft, ob diese unter den gegebenen Umständen anwendbar sind. Für jeden anwendbaren Use Case 
wird ebenfalls eine semi-quantitative Evaluation auf einer Skala von 1 bis 5 vorgenommen.

### Nutzen einer Kategorie:
Der Nutzen einer Kategorie wird auf Basis der globalen Nutzenkriterien Versorgungssicherheit, Umweltauswirkungen, 
Automatisierungsgrad und Energieeffizienz ermittelt. Dafür werden die, vom Nutzer vergebenen Gewichtungen mit den hinterlegten 
Werten aus dem [vordefinierten Kategorieranking](./data/Vordefiniertes_Kategorie_Ranking.csv) multipliziert und durch den 
maximalen Gewichtswert 5 geteilt. Die gemittelte Summe dieser Kriterienwerte stellt den Nutzen der für die jeweilige Kategorie dar. 
Das vordefinierte Kategorieranking wurde im Projekt auf Basis einer Expertenumfrage ermittelt, bei der Experten
des Fraunhofer IEE, Fraunhofer IBP und der AGFW die 5 ML Use Case Kategorien hinsichtlich jedes Kriteriums mit einer Zahl
von 1 bis 5 eingeschätzt haben. Die Mittelwerte Experteneinschätzungen für jede Kategorie und jedes Kriterium ergibt das 
vordefinierte Kategorieranking.

### Aufwand einer Kategorie:
Analog zum Nutzen wird der Aufwand einer Kategorie auf Basis der vom Nutzer vorgenommenen Gewichtungen und den Werten des 
[vordefinierten Kategorierankings](./data/Vordefiniertes_Kategorie_Ranking.csv) zu den Kriterien Kostenaufwand, Zeitaufwand 
und Personalaufwand ermittelt.

### Risiko einer Kategorie:
Der Risikowert einer Kategorie basiert auf den Antworten des Nutzers zu den kategoriespezifische Risikofragen. 
Diese stellen ausschließlich Ja-Nein-Fragen dar, wobei der risikoerhöhenden Antwort der Wert 5 zugewiesen wird und der 
risikomindernden Antwort der Wert 1. Der Risikowert einer Kategorie ist der Mittelwert aller Antworten zu den kategoriespezifischen Risikofragen.

### Anwendbarkeit eines Use Cases:
In bestimmten Konstellationen kann es dazu kommen, dass Use Cases nicht umsetzbar sind. Beispiel: Antwort „Nein“ auf die 
Frage „Haben Sie Zugriff auf Druckdaten in Haus-stationen?“ und Antwort „Nein“ auf die Frage 
„Würden Sie Druckdaten in Hausstationen erheben, um einen ML Use Case zu ermöglichen?“. 
In diesem Fall könnten Use Cases, die diese Daten benötigen, nicht umgesetzt werden. 
Um solche Fälle abzudecken, sind für jeden Use Case Bedingungen definiert, die zur Nichtumsetzbarkeit führen. 
Falls mindestens eine dieser Bedingungen erfüllt ist, wird der Use Case nicht weiter bewertet und er erhält als Nutzen-, Aufwands- und Riskowert jeweils die 0.
Im Fall der Anwendbarkeit wird die Auswertung wie folgt durchgeführt:

#### Nutzen eines Use Cases:
Der Nutzen eines Use Cases wird auf Basis der lokalen Kriterien der Kategorie des Use Cases ermittelt. 
Analog zur Bestimmung des Nutzens von Kategorien werden hier die vom Nutzer vorgenommenen Gewichtungen der Kriterien mit dem
vordefiniertem Hintergrundwissen kombiniert. Auf Basis der Ergebnisse der Literaturrecherche und Einschätzungen des 
Projektbearbeitungsteams wurde für jeden Use Case und alle zugehörigen lokalen Kriterien ein Wert zwischen 1 und 5 festgelegt. 
Für die Einschätzung des ML4FW-Use Cases zur Reglerparameteroptimierung wurden die Perspektiven aus der Erarbeitung der 
Simulationsmodelle, der ML-Umsetzung und der wissenschaftlichen Begleitung vereint, um für jedes lokale Krtierium einen 
zwischen 1 und 5 festzulegen. Der finale Nutzen eines Use Cases wird durch die gemittelte Summe der gewichteten Kriterienwerte dargestellt.

#### Aufwand eines Use Cases:
Der Aufwand eines ML Use Cases wird auf Basis der Aufwandskriterien aus der [Tabelle](#lokale-aufwandskriterien), vorgenommen. 
Hierbei wurden weitere Einschätzungen der Use Cases durch das Projektbearbeitungsteam vorgenommen und Werte von 1 bis 5 
für jedes Kriterium festgelegt. Dieses Hintergrundwissen wird mit den Angaben des Nutzers zu den Fragen zur 
Datenverfügbarkeit und potenziellen Datenerhebungs- und Datenspeicherungsaufwänden kombiniert. Jede dieser Fragen ist 
einem der Aufwandskriterien zugewiesen und für jede Antwort dieser Fragen ist ein Wert zwischen 1 und 5 festgelegt, dessen 
Höhe davon abhängt, ob diese Antwort zur Erhöhung des Aufwands führt oder nicht. Beispiel: Der Nutzer verfügt über keine 
Druckdaten von Hausstationen, ist aber bereit für die Umsetzung eines ML Use Cases solche Daten zu erheben. 
In diesem Fall erhöht sich der Datenerhebungsaufwand für alle Use Cases, die diese Daten benötigen. 
Deswegen ist der Antwort „Nein“ auf die Frage „Haben Sie Zugriff auf Druckdaten in Hausstationen?“ mit dem Datenerhebungsaufwand 5 verknüpft. 
Für jedes Aufwandskriterium wird der Mittelwert aller für den jeweiligen Use Case relevanten Fragen, die diesem Kriterium zugewiesen sind, gebildet
und mit der Einschätzung aus dem Hintergrundwissen gewichtet. Der Gesamtaufwandswert eines Use Cases ergibt sich schließlich 
aus dem Mittelwert aller gewichteten Kriterienwerte.

#### Risiko eines Use Cases:
Das Risiko eines Use Cases wird ermittelt, indem der Durchschnitt des entsprechenden Kategorierisikos und einer festgelegten 
Bewertung durch das Projektbearbeitungsteam auf einer Skala von 1 bis 5 herangezogen werden.

## Ergebnisdarstellung

Die Visualisierung der Ergebnisse zur Kategorie- und Use Case-Bewertung wird in Form von zweistufigen Koordinatensystemen vorgenommen. 
Zuerst werden die Kategorien als Punkte in einem Koordinatensystem mit der x-Achse „Nutzen“ und der y-Achse „Aufwand“ dargestellt. 
Die Färbung der Punkte spiegelt das Kategorierisiko wider. Nach der Visualisierung der Kategorien werden analoge Grafiken für die Use Cases 
jeder Kategorie angelegt. Hierbei ist allerdings anzumerken, dass sich die Nutzen- und Aufwandswerte in den Use Case Grafiken 
aufgrund ihrer Zusammensetzung aus anderen Kriterien von den Nutzen- und Aufwandswerten aus den anderen Grafiken unterscheiden 
und somit keine Use Case-Vergleiche zwischen verschiedenen Kategorien möglich sind. 

# Abgebildete ML Use Cases

| Use Case                                                                                      | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Quelle                                                                                                               | Kategorie |
|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|----------|
| Wärmelastprognosen anhand detaillierter Netzdaten                                           | Wärmelastvorhersage für gesamten Fernwärmenetz mithilfe von mehreren LSTM-Architekturen                                                                                                                                                                                                                                                                                                                                                                                               | [Link 1](https://doi.org/10.1016/j.arcontrol.2022.03.009) und [Link 2](https://doi.org/10.1016/j.ifacol.2021.08.044) | WBP      |
| Wärmelastprognose für Fernwärmenetze mit Berücksichtigung der Netzstruktur                  | Prognose eines Gesamtnetzes anhand Wärmelastprofile einzelner Gebäude und Netzwerktopologie mit Graph Recurrent Neural Networks                                                                                                                                                                                                                                                                                                                                                       | [Link](https://doi.org/10.1016/j.apenergy.2023.121753)                                                               | WBP      |
| Wärmelastprognose für einzelne Gebäude und Stadtviertel                                      | Kurzfristige Lastprognose anhand historischer Last- und Wetterdaten mithilfe von ANN in Kombination mit multipler linearer Regression                                                                                                                                                                                                                                                                                                                                                 | [Link](https://doi.org/10.1016/j.energy.2023.129866)                                                                 | WBP      |
| Echtzeitprognose für Wärmelasten in Fernwärmenetzen                                          | Kurzfristige Wärmelastprognosen in Echtzeit mithilfe von LSTM                                                                                                                                                                                                                                                                                                                                                                                                                         | [Link](https://doi.org/10.3384/ecp200050)                                                                            | WBP      |
| Prognose für Wärmespeicher und Spitzenlastmanagement                                          | Vorhersage der Wärmelasten und Speicherfüllstände zur Spitzenlastkappung mit incremental learning LSTM                                                                                                                                                                                                                                                                                                                                                                                | [Link](https://doi.org/10.1016/j.energy.2024.131690)                                                                 | WBP      |
| Haushaltsbezogene Wärmelastprognose für individuelle Gebäude                                  | Wärmebedarfsprognose auf Haushaltsebene mithilfe von Support Vector Regression (SVR) und Partikelschwarmoptimierung (PSO)                                                                                                                                                                                                                                                                                                                                                             | [Link](https://arxiv.org/pdf/2112.01908)                                                                             | WBP      |
| Anomalieerkennung durch Ensemblemodellierung                                                  | Dieser Use Case setzt einfache ML-Modelle für jede einzelne Hausstation ein und führt parallel dazu ein Clustering der Hausstationen in verschiedene Gruppen durch. Auf Basis dieser zwei Informationslevel kann ein Ensemble Modell erstellt werden, welches das Erkennen von fehlerhaften Hausstationen ermöglicht.                                                                                                                                                                 | [Link](https://doi.org/10.1016/j.eswa.2022.116864)                                                                   | InHAST   |
| Anomalie-erkennung mithilfe von Clusteringmethoden                                            | Durch die Anwendung von Clustering-Verfahren auf Basis von Zeitreihendaten der HASTs werden Ausreißer-HASTs identifiziert.                                                                                                                                                                                                                                                                                                                                                            | [Link](https://doi.org/10.1109/FMEC62297.2024.10710205)                                                              | InHAST   |
| Rekonstruktionsbasierte Normalverhaltensmodelle                                              | In diesem Use Case werden auf Basis der Wärmeleistungsdaten Abweichungen vom normalen Verhalten von HASTs durch die Anwendung von rekonstruktionsbasierten Normalverhaltensmodellen wie beispielsweise Autoencodern ermöglicht. Diese erlernen das normale Verhalten auf Basis von historischen Daten der HASTs.                                                                                                                                                                      | [Link](https://doi.org/10.1109/ICIEA48937.2020.9248108)                                                              | InHAST   |
| Regressionsbasierte Normalverhaltensmodelle                                                  | Durch die Nutzung regressionsbasierter Modelle wird das Verhalten von HASTs basierend auf einem bereitgestellten Datensatz erlernt. Durch den Abgleich von weiteren Betriebsdaten mit der Modellvorhersage wird die Erkennung von Abweichungen und Fehlern ermöglicht.                                                                                                                                                                                                                | [Link](https://doi.org/10.34641/clima.2022.4)                                                                        | InHAST   |
| Leckagenerkennung auf Basis von Infrarotbildern                                              | Automatisierte ML-Bildanalyseverfahren werden genutzt, um Leckagen auf Infrarotbildern zu lokalisieren.                                                                                                                                                                                                                                                                                                                                                                               | [Link](https://doi.org/10.1016/j.autcon.2024.105709)                                                                 | InRN     |
| Leckagenerkennung auf Basis von Drucksensorik                                                | Eine Kombination einer hydraulischen Simulation mit einem auf XGBoost basierenden Klassifikator wird genutzt, um Leckagen zu identifizieren und dem korrekten Abschnitt des Rohrnetzes zuzuordnen.                                                                                                                                                                                                                                                                                    | [Link](https://doi.org/10.1016/j.enbuild.2020.110161)                                                                | InRN     |
| Klassifikation von Rohrzuständen auf Basis von Akustik- und Vibrationssignalen              | Dieser Use Case nutzt direkte Klassifikationsverfahren wie beispielsweise Support Vector Machines für die Zuordnung von akustischen Messwerten zu festgelegten Rohrzuständen.                                                                                                                                                                                                                                                                                                         | [Link](https://doi.org/10.1016/j.measurement.2023.11338)                                                             | InRN     |
| Optimierung des Netzbetriebs mithilfe ML-basierter Netzsimulation                            | Durch die Verwendung eines Reinforcement Learning Ansatzes, in Kombination mit Hintergrundwissen über die Netztopologie wird ein effizientes und dynamisches Simulationsmodell erstellt, welches anschließend verwendet wird, um den Fernwärmenetzbetrieb hinsichtlich Kosten der Wärmeproduktion und Wärmeeffizienz zu optimieren.                                                                                                                                                   | [Link](https://doi.org/10.1109/TCST.2024.335)                                                                        | BeWN     |
| Spitzenlastreduzierung                                                                      | Dieser Use Case nutzt einen Reinforcement Learning Ansatz, der auf Basis eines Netzmodells, einer thermodynamischen Modellierung der Gebäude im Fernwärmenetz und eines agentenbasierten Nutzerkomfortmodells eine optimale Strategie für die Reduktion von Spitzenlasten ermittelt.                                                                                                                                                                                              | [Link](https://doi.org/10.1016/j.engappai.202)                                                                       | BeWN     |
| Flexibilitätsnutzung von Gebäuden durch die Steuerung der Wärmezufuhr                       | In diesem Use Case wird ein Reinforcement Learning Algorithmus verwendet, um thermostatgesteuerte Wärmespeichermöglichkeiten wie Gebäudehüllen im Fernwärmenetz zu flexibilisieren. Ziel ist die Nutzung dieser Flexibilitäten für Spitzenlastreduktionen und/oder Energie-Arbitrage.                                                                                                                                                                                                 | [Link](https://doi.org/10.1016/j.enbuild.2017.08.052)                                                                | BeWN     |
| ML-Ersatzmodell für thermo-hydraulische Simulationen                                         | Dieser Use Case verwendet ein Graph-Neural-Network, um bestehende aufwändige thermo-hydraulische Simulationsmodelle durch ein schnelleres, effizienteres ML-Modell zu ersetzen und Durchflussraten sowie Temperaturen an verschiedenen Stellen im Netz zu simulieren.                                                                                                                                                                                                                 | [Link](https://hal.science/CETHIL/hal-04462676v1)                                                                    | BeWN     |
| ML-unterstützte Regleroptimierung                                                            | Dieser Use Case nutzt die Anwendbarkeit und Effektivität von Methoden des maschinellen Lernens (ML) für das Auto- und Continuous-Commissioning von Regelgeräten an realen Fernwärme-Hausstationen. Damit wird die automatisierte Anpassung von Regelparametern, die sich zunächst in der Werkeinstellung befinden, an die individuellen Betriebsbedingungen des jeweiligen Gebäudes erreicht. Dies stellt sicher, dass eine optimale Regelung der Hausstationen (HAST) erreicht wird. | Abschlussbericht ML4FW (Wird eingefügt sobald veröffentlicht)                                                        | BeHAST   |
| ML-basierte Optimierung von Fernwärme-Sekundärkreisen                                       | Dieser Use Case befasst sich mit der Erstellung eines ML-Modells für die optimierte Steuerung des Wärmeflusses vom Primärkreislauf in den Sekundärkreislauf durch die automatisierte Steuerung von Ventilen. Das Ventilsteuerungsmodell wird dabei auf Basis historischer Ventileinstellungsdaten im Kontext mit der Wetterdaten erstellt und mit einem ML-Vorhersagemodell für die Vorlauftemperatur im Sekundärkreis bei verschiedenen Ventileinstellungen kombiniert.              | [Link](https://doi.org/10.1016/j.energy.2021.122061)                                                                 | BeHAST   |

# Lizenz

Der ML4FW Fragebogen kann unter der [MIT-Lizenz](./LICENSE) genutzt werden.
