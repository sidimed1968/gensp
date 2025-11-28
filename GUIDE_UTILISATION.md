# 📖 Guide d'Utilisation - Système de Gestion des Logements

## دليل الاستخدام - نظام إدارة المساكن

---

## 🇫🇷 FRANÇAIS

### 🚀 Démarrage Rapide

1. **Ouvrir un terminal** dans le dossier du projet

2. **Lancer l'application** avec l'une des commandes suivantes :
   ```bash
   streamlit run app.py
   ```
   
   Ou simplement :
   ```bash
   ./run_app.sh
   ```

3. **Ouvrir le navigateur** à l'adresse : `http://localhost:8501`

### 📊 Tableau de Bord

**Accès** : Cliquer sur "📊 Tableau de Bord" dans le menu latéral

**Fonctionnalités** :
- Vue d'ensemble des statistiques (total, îlots, départements)
- Graphiques interactifs de répartition
- Carte générale de tous les logements

### 📋 Liste des Logements

**Accès** : Cliquer sur "📋 Liste des Logements"

**Fonctionnalités** :
1. **Filtres** : Utilisez les filtres en haut pour affiner la recherche
   - Par îlot (A, B, C, etc.)
   - Par département
   - Par profession
   - Recherche textuelle globale

2. **Sélection des colonnes** : Choisissez les colonnes à afficher

3. **Actions sur un logement** :
   - ✏️ **Modifier** : Éditer les informations
   - 🗺️ **Voir sur carte** : Localiser sur la carte GPS
   - 🗑️ **Supprimer** : Retirer de la base

4. **Exportation** : Cliquer sur "📥 Exporter les données" pour sauvegarder en Excel

### ➕ Ajouter un Logement

**Accès** : Cliquer sur "➕ Ajouter un Logement"

**Étapes** :
1. Remplir les champs obligatoires (marqués *)
   - Îlot
   - Numéro de logement
   - Nom de l'affectaire

2. Compléter les informations optionnelles
   - NNI, profession, département
   - Téléphone, statut d'activité
   - Coordonnées GPS

3. Cliquer sur "💾 Enregistrer"

### ✏️ Modifier un Logement

**Accès** : 
- Depuis la liste → Sélectionner un logement → Cliquer sur "✏️ Modifier"
- Ou via le menu "✏️ Modifier un Logement"

**Étapes** :
1. Modifier les champs souhaités
2. Cliquer sur "💾 Enregistrer" pour confirmer
3. Ou "❌ Annuler" pour abandonner

### 🗺️ Cartographie GPS

**Accès** : Cliquer sur "🗺️ Cartographie GPS"

**Fonctionnalités** :

1. **Carte interactive**
   - Zoom avec molette de souris ou boutons +/-
   - Déplacement en cliquant-glissant
   - Plein écran possible

2. **Marqueurs colorés**
   - Chaque îlot a sa couleur
   - Cliquer sur un marqueur pour voir les détails
   - Survoler pour un aperçu rapide

3. **Filtres dynamiques**
   - Sélectionner îlot, département, profession
   - La carte se met à jour automatiquement
   - Compteur de logements affichés

4. **Légende**
   - En bas à gauche de la carte
   - Identifie la couleur de chaque îlot

### 💾 Import/Export

**Accès** : Cliquer sur "💾 Import/Export"

**Import** :
1. Cliquer sur "Parcourir" pour sélectionner un fichier Excel
2. Cliquer sur "Importer les données"
3. Attendre la confirmation

**Export** :
1. Entrer un nom de fichier (optionnel)
2. Cliquer sur "Exporter les données"
3. Télécharger le fichier généré

### 📜 Historique

**Accès** : Cliquer sur "📜 Historique"

**Contenu** :
- Journal de toutes les modifications
- Actions : CREATE, UPDATE, DELETE, IMPORT, EXPORT
- Date et heure de chaque opération
- Détails des modifications

### 🖨️ Impression

**Pour imprimer une liste** :
1. Afficher la liste avec les filtres souhaités
2. Sélectionner les colonnes à imprimer
3. Cliquer sur "🖨️ Préparer impression"
4. Utiliser Ctrl+P (ou Cmd+P sur Mac)

### 🌐 Changement de Langue

**Pour passer en arabe** :
- Dans la barre latérale, sélectionner "العربية"
- L'interface se met à jour automatiquement

---

## 🇸🇦 العربية (ARABE)

### 🚀 البدء السريع

1. **افتح terminal** في مجلد المشروع

2. **قم بتشغيل التطبيق** باستخدام أحد الأوامر التالية:
   ```bash
   streamlit run app.py
   ```
   
   أو ببساطة:
   ```bash
   ./run_app.sh
   ```

3. **افتح المتصفح** على العنوان: `http://localhost:8501`

### 📊 لوحة المعلومات

**الوصول**: انقر على "📊 لوحة المعلومات" في القائمة الجانبية

**الوظائف**:
- نظرة عامة على الإحصائيات (الإجمالي، الجزر، الأقسام)
- رسوم بيانية تفاعلية للتوزيع
- خريطة عامة لجميع المساكن

### 📋 قائمة المساكن

**الوصول**: انقر على "📋 قائمة المساكن"

**الوظائف**:
1. **الفلاتر**: استخدم الفلاتر في الأعلى لتحسين البحث
   - حسب الجزيرة (A، B، C، إلخ)
   - حسب القسم
   - حسب المهنة
   - البحث النصي الشامل

2. **اختيار الأعمدة**: اختر الأعمدة المراد عرضها

3. **الإجراءات على المسكن**:
   - ✏️ **تعديل**: تحرير المعلومات
   - 🗺️ **عرض على الخريطة**: تحديد الموقع على خريطة GPS
   - 🗑️ **حذف**: إزالة من قاعدة البيانات

4. **التصدير**: انقر على "📥 تصدير البيانات" للحفظ في Excel

### ➕ إضافة مسكن

**الوصول**: انقر على "➕ إضافة مسكن"

**الخطوات**:
1. املأ الحقول الإلزامية (المميزة بـ *)
   - الجزيرة
   - رقم المسكن
   - اسم المستفيد

2. أكمل المعلومات الاختيارية
   - رقم التعريف الوطني، المهنة، القسم
   - الهاتف، حالة النشاط
   - إحداثيات GPS

3. انقر على "💾 حفظ"

### ✏️ تعديل مسكن

**الوصول**:
- من القائمة → حدد مسكنًا → انقر على "✏️ تعديل"
- أو عبر القائمة "✏️ تعديل مسكن"

**الخطوات**:
1. قم بتعديل الحقول المطلوبة
2. انقر على "💾 حفظ" للتأكيد
3. أو "❌ إلغاء" للإلغاء

### 🗺️ الخريطة GPS

**الوصول**: انقر على "🗺️ الخريطة"

**الوظائف**:

1. **خريطة تفاعلية**
   - التكبير/التصغير بعجلة الماوس أو الأزرار +/-
   - التنقل بالنقر والسحب
   - وضع ملء الشاشة متاح

2. **العلامات الملونة**
   - لكل جزيرة لون خاص
   - انقر على علامة لرؤية التفاصيل
   - مرر الماوس للحصول على معاينة سريعة

3. **الفلاتر الديناميكية**
   - حدد الجزيرة، القسم، المهنة
   - يتم تحديث الخريطة تلقائيًا
   - عداد المساكن المعروضة

4. **وسيلة الإيضاح**
   - أسفل يسار الخريطة
   - يحدد لون كل جزيرة

### 💾 الاستيراد/التصدير

**الوصول**: انقر على "💾 استيراد/تصدير"

**الاستيراد**:
1. انقر على "تصفح" لاختيار ملف Excel
2. انقر على "استيراد البيانات"
3. انتظر التأكيد

**التصدير**:
1. أدخل اسم الملف (اختياري)
2. انقر على "تصدير البيانات"
3. قم بتنزيل الملف المُنشأ

### 📜 السجل

**الوصول**: انقر على "📜 السجل"

**المحتوى**:
- سجل جميع التعديلات
- الإجراءات: CREATE، UPDATE، DELETE، IMPORT، EXPORT
- تاريخ ووقت كل عملية
- تفاصيل التعديلات

### 🖨️ الطباعة

**لطباعة قائمة**:
1. اعرض القائمة بالفلاتر المطلوبة
2. حدد الأعمدة المراد طباعتها
3. انقر على "🖨️ تحضير للطباعة"
4. استخدم Ctrl+P (أو Cmd+P على Mac)

### 🌐 تغيير اللغة

**للتبديل إلى الفرنسية**:
- في الشريط الجانبي، حدد "Français"
- يتم تحديث الواجهة تلقائيًا

---

## 🆘 Aide et Support / المساعدة والدعم

### Problèmes courants / المشاكل الشائعة

**L'application ne démarre pas / التطبيق لا يبدأ**
```bash
# Vérifier les dépendances / تحقق من التبعيات
pip install -r requirements.txt
```

**Le fichier Excel ne s'importe pas / لا يتم استيراد ملف Excel**
- Vérifier que le fichier contient les bonnes colonnes
- تأكد من أن الملف يحتوي على الأعمدة الصحيحة

**La carte ne s'affiche pas / لا تظهر الخريطة**
- Vérifier la connexion Internet
- تحقق من اتصال الإنترنت

### Contact / الاتصال

Pour toute question : contactez l'administrateur système
لأي سؤال: اتصل بمسؤول النظام

---

**© 2024 - Système de Gestion des Logements - Nouakchott, Mauritanie**

**نظام إدارة المساكن - نواكشوط، موريتانيا**
