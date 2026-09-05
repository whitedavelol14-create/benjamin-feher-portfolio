import { defineConfig } from "tinacms";

// Tina CMS config — Benjamin Fehér portfolio
// Szerkesztő: Tina Cloud (app.tina.io) → commit a main ágra → GitHub Pages auto-deploy.

export default defineConfig({
  branch: "main",
  build: {
    outputFolder: "admin",
    publicFolder: "",
  },
  schema: {
    collections: [
      {
        name: "content",
        label: "Oldal tartalom",
        path: "content",
        format: "json",
        ui: { allowedActions: { create: false, delete: false } },
        fields: [
          {
            type: "object",
            label: "Fejléc / Hero",
            name: "site",
            fields: [
              { type: "string", label: "Brand (fix)", name: "brand", ui: { readOnly: true } },
              { type: "string", label: "Szerep / alcím", name: "role" },
              { type: "string", label: "Név sor 1", name: "hero_line1" },
              { type: "string", label: "Név sor 2", name: "hero_line2" },
              { type: "string", label: "Hero leírás", name: "tagline", ui: { component: "textarea" } },
              {
                type: "object", label: "Reel gomb", name: "reel",
                fields: [
                  { type: "string", label: "Felirat", name: "label" },
                  { type: "string", label: "Hossz", name: "duration" },
                  { type: "string", label: "Link", name: "href" },
                ],
              },
              { type: "string", label: "E-mail", name: "email" },
              { type: "string", label: "Kontakt szöveg", name: "contact_line" },
              { type: "string", label: "Helyszín / elérhetőség", name: "location" },
              {
                type: "object", label: "HUD értékek (kamera)", name: "hud",
                fields: [
                  { type: "string", label: "FPS", name: "fps" },
                  { type: "string", label: "Shutter", name: "shutter" },
                  { type: "string", label: "Iris", name: "iris" },
                  { type: "string", label: "EI", name: "ei" },
                  { type: "string", label: "ND", name: "nd" },
                  { type: "string", label: "CAM", name: "cam" },
                  { type: "string", label: "FCL", name: "fcl" },
                  { type: "string", label: "Media", name: "media" },
                  { type: "string", label: "TC kezdőérték", name: "tc_start" },
                ],
              },
            ],
          },
          {
            type: "object",
            label: "About",
            name: "about",
            fields: [
              { type: "string", label: "Címke", name: "label" },
              { type: "string", label: "Helyszín sor", name: "loc" },
              { type: "string", label: "Nagy mondat", name: "pull", ui: { component: "textarea" } },
              {
                type: "string", label: "Bekezdések", name: "paragraphs", list: true,
                ui: { component: "textarea" },
              },
              { type: "string", label: "Kollaborátorok sor", name: "collaborators" },
            ],
          },
          {
            type: "object",
            label: "Kategóriák és projektek",
            name: "categories",
            list: true,
            ui: { itemProps: (item) => ({ label: item?.title }) },
            fields: [
              { type: "string", label: "Cím", name: "title" },
              { type: "string", label: "Darabszám", name: "count" },
              { type: "string", label: "Alcím", name: "desc" },
              { type: "string", label: "Azonosító (id)", name: "id", ui: { readOnly: true } },
              {
                type: "object", label: "Projektek", name: "projects", list: true,
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", label: "Cím", name: "title" },
                  { type: "string", label: "Év", name: "year" },
                  { type: "string", label: "Meta (műfaj · szerep)", name: "meta" },
                  { type: "string", label: "Link", name: "href" },
                  { type: "boolean", label: "Placeholder címke", name: "placeholder" },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
});
